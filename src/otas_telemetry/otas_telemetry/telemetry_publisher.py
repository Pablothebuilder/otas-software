from datetime import datetime, timezone

import rclpy
from mavros_msgs.msg import State
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.subscription import Subscription
from std_msgs.msg import String


class TelemetryPublisher(Node):
    def __init__(self) -> None:
        super().__init__("telemetry_publisher")
        self._state: State | None = None
        self._telemetry_publisher: Publisher = self.create_publisher(
            String, "/otas/telemetry", 10
        )
        self._state_subscription: Subscription = self.create_subscription(
            State, "/mavros/state", self._on_state, 10
        )
        self.create_timer(1.0, self._publish_telemetry)

    def _on_state(self, state: State) -> None:
        self._state = state

    def _publish_telemetry(self) -> None:
        state = self._state
        health = (
            "WAITING_FOR_MAVROS"
            if state is None
            else "OK"
            if state.connected
            else "DISCONNECTED"
        )
        flight_mode = (
            state.mode if state is not None and state.mode else "UNKNOWN"
        )
        armed = state.armed if state is not None else False
        timestamp = (
            datetime.now(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )

        message = String()
        message.data = (
            f"OTAS_HEARTBEAT: {health} | timestamp={timestamp} "
            f"| flight_mode={flight_mode} | armed={str(armed).lower()}"
        )
        self._telemetry_publisher.publish(message)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = TelemetryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
