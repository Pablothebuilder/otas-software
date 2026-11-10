import time

import rclpy
from mavros_msgs.msg import State
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from otas_telemetry.telemetry_publisher import TelemetryPublisher


def test_publishes_heartbeat_with_mavros_state():
    rclpy.init()
    telemetry_node = TelemetryPublisher()
    test_node = Node("telemetry_publisher_test")
    received_messages = []
    executor = SingleThreadedExecutor()

    def receive_telemetry(message: String) -> None:
        received_messages.append(message.data)

    state_publisher = test_node.create_publisher(State, "/mavros/state", 10)
    test_node.create_subscription(
        String, "/otas/telemetry", receive_telemetry, 10
    )
    executor.add_node(telemetry_node)
    executor.add_node(test_node)

    state = State()
    state.connected = True
    state.armed = True
    state.mode = "GUIDED"

    try:
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline and not any(
            "OTAS_HEARTBEAT: OK" in message for message in received_messages
        ):
            state_publisher.publish(state)
            executor.spin_once(timeout_sec=0.1)

        heartbeat = next(
            (
                message
                for message in received_messages
                if "OTAS_HEARTBEAT: OK" in message
            ),
            None,
        )
        assert heartbeat is not None
        assert "flight_mode=GUIDED" in heartbeat
        assert "armed=true" in heartbeat
        assert "timestamp=" in heartbeat
    finally:
        executor.shutdown()
        telemetry_node.destroy_node()
        test_node.destroy_node()
        rclpy.shutdown()
