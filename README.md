# OTAS Drone Mission

OTAS is a ROS 2 and ArduPilot SITL development project for drone simulation.
The verified simulation stack uses Gazebo, ArduPilot SITL/MAVProxy, MAVROS, and
the OTAS telemetry publisher. See [SETUP.md](SETUP.md) for the complete
Windows WSL 2 runbook, including container setup, simulation bring-up,
takeoff/landing, recording, and troubleshooting.

## T1 telemetry and heartbeat

The `otas_telemetry` ROS 2 package publishes a 1 Hz
`std_msgs/msg/String` heartbeat on `/otas/telemetry`, containing a UTC
timestamp, flight mode, armed state, and health status. Health is
`OTAS_HEARTBEAT: OK` only while the latest MAVROS state reports a connected
vehicle; otherwise the node reports `WAITING_FOR_MAVROS` or `DISCONNECTED`.

In the verified setup, MAVROS publishes state on `/state`, while the telemetry
node subscribes to `/mavros/state`. Remap the subscription when launching the
publisher:

```bash
ros2 run otas_telemetry telemetry_publisher --ros-args -r /mavros/state:=/state
```

Expected output while connected resembles:

```text
OTAS_HEARTBEAT: OK | timestamp=2026-01-01T12:00:00.000Z | flight_mode=GUIDED | armed=true
```

For the SITL takeoff/landing test, issue these commands one at a time at the
MAVProxy `STABILIZE>` prompt:

```text
mode guided
arm throttle
takeoff 5
```

After confirming the climb and telemetry (`flight_mode=GUIDED`,
`armed=true`), land with:

```text
mode land
```

This is a simulation test, not a real-flight procedure. Start a continuous
`ros2 topic echo /otas/telemetry` before takeoff to observe the changes. The
runbook shows how to record the stream to a file.

## Integration tests

Inside the container, from `/workspace`, after sourcing ROS and the built
workspace:

```bash
cd /workspace
source /opt/ros/humble/setup.bash
source install/setup.bash
pytest tests/
```
