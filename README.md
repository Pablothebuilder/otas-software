# OTAS Drone Mission

## T1 Telemetry and Heartbeat

The `otas_telemetry` ROS 2 package publishes a 1 Hz heartbeat on
`/otas/telemetry`. Each `std_msgs/msg/String` message includes a UTC timestamp,
the latest MAVROS flight mode and arming state, and health status. Health is
`OK` only while the latest `/mavros/state` reports a connected vehicle.

Build and run inside the development container:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run otas_telemetry telemetry_publisher
```

In another container terminal, inspect the output:

```bash
ros2 topic echo /otas/telemetry
```

The MAVROS bridge must publish `/mavros/state` for the heartbeat to report
`OTAS_HEARTBEAT: OK`; until then it reports `WAITING_FOR_MAVROS`.

Run the ROS integration test from the workspace root after sourcing ROS and
the workspace:

```bash
pytest tests/
```
