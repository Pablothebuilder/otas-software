# OTAS Simulation Runbook

This runbook brings up the OTAS development container, Gazebo, ArduPilot SITL,
MAVROS, and the OTAS telemetry publisher, then records a simulated takeoff and
landing. This is a **SITL simulation test only**, not a procedure for flying a
real vehicle.

## Prerequisites

The verified GUI setup is **Windows with WSL 2 (Ubuntu 22.04), Docker Desktop,
and WSLg**:

1. Install WSL 2 with Ubuntu 22.04 (`wsl --install -d Ubuntu-22.04`).
2. Install Docker Desktop and enable WSL 2 integration for the Ubuntu
   distribution.
3. Clone this repository into WSL, for example at `~/otas-software`.
4. Open seven WSL terminal tabs in the repository directory. Gazebo requires
   the WSLg GUI display integration provided by this setup.

The current Compose configuration mounts WSLg paths. The old macOS/XQuartz
`docker compose run --rm` instructions are not a verified way to run this
complete stack.

## Start the container and build the workspace

In Tab 1, start the container and allow the ArduPilot checkout inside it to be
used by Git:

```bash
cd ~/otas-software
docker compose up -d
docker compose exec dev-environment bash -lc \
  'git config --global --get-all safe.directory | grep -Fxq /home/ardupilot/ardupilot || git config --global --add safe.directory /home/ardupilot/ardupilot'
```

Build the ROS workspace before starting the telemetry process:

```bash
docker compose exec dev-environment bash -lc \
  'source /opt/ros/humble/setup.bash && cd /workspace && colcon build --symlink-install'
```

Optionally verify the tools inside the container:

```bash
docker compose exec dev-environment bash -lc \
  'source /opt/ros/humble/setup.bash && ros2 node list && gz sim --version && flake8 --version && pytest --version && cpplint --version'
```

## Start the simulation stack

Run each command in its own tab from `~/otas-software`. Keep the Gazebo, SITL,
MAVROS, telemetry, and echo processes running while testing.

**Tab 2 — Gazebo**

```bash
cd ~/otas-software
docker compose exec -it dev-environment bash -lc \
  'gz sim -v4 -r /opt/ardupilot_gazebo/worlds/iris_runway.sdf'
```

**Tab 3 — ArduPilot SITL and MAVProxy**

```bash
cd ~/otas-software
docker compose exec -it dev-environment bash -lc \
  'cd /opt/ardupilot && Tools/autotest/sim_vehicle.py -j 2 -v ArduCopter -f gazebo-iris --model JSON --console --map'
```

Wait for MAVProxy to show `Detected vehicle 1:1` and the `STABILIZE>` prompt.

**Tab 4 — MAVROS**

```bash
cd ~/otas-software
docker compose exec -it dev-environment bash -lc \
  'source /opt/ros/humble/setup.bash && ros2 launch mavros apm.launch fcu_url:=udp://:14550@'
```

Wait for MAVROS to log `CON: Got HEARTBEAT, connected. FCU: ArduPilot`.

**Tab 5 — OTAS telemetry**

```bash
cd ~/otas-software
docker compose exec -it dev-environment bash -lc \
  'source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 run otas_telemetry telemetry_publisher --ros-args -r /mavros/state:=/state'
```

The remap is required for this setup: MAVROS publishes state on `/state`, while
the telemetry node subscribes to `/mavros/state`. The telemetry process may
remain quiet; observe its topic in Tab 7.

**Tab 6 — Continuously watch MAVROS state**

```bash
cd ~/otas-software
docker compose exec dev-environment bash -lc \
  'source /opt/ros/humble/setup.bash && ros2 topic echo /state'
```

**Tab 7 — Display and record OTAS telemetry**

Start this before takeoff. It continuously displays telemetry and writes it to
`~/otas-software/otas-takeoff-telemetry.yaml` on the host through the workspace
mount. It intentionally does not use `--once`. If that filename already
exists, change it in the command before running so you do not overwrite the
existing recording.

```bash
cd ~/otas-software
docker compose exec dev-environment bash -lc \
  'source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 topic echo /otas/telemetry | tee /workspace/otas-takeoff-telemetry.yaml'
```

## Simulated takeoff and landing

At the `STABILIZE>` prompt in Tab 3, enter these commands **one at a time**:

```text
mode guided
arm throttle
takeoff 5
```

Observe the climb in Gazebo and confirm telemetry changes to
`flight_mode=GUIDED` and `armed=true`. To land, enter this at the MAVProxy
prompt:

```text
mode land
```

Observe the landing in Gazebo. Tab 7 continues recording the mode and arming
state changes through landing.

## Expected success indicators

- Gazebo loads the `ArduPilotPlugin` and displays the Iris on the runway.
- SITL detects vehicle `1:1` and MAVProxy reaches the `STABILIZE>` prompt.
- MAVROS reports `CON: Got HEARTBEAT, connected. FCU: ArduPilot`.
- `/state` reports `connected: true`.
- `/otas/telemetry` reports `OTAS_HEARTBEAT: OK` and shows a UTC timestamp,
  flight mode, and armed state.
- The telemetry recording captures the mode and armed-state changes during
  takeoff and landing.

Each telemetry message is published once per second as a
`std_msgs/msg/String`, for example:

```text
OTAS_HEARTBEAT: OK | timestamp=2026-01-01T12:00:00.000Z | flight_mode=GUIDED | armed=true
```

## Shutdown

Stop the live commands in Tabs 2–7 with `Ctrl+C`, then stop the container:

```bash
cd ~/otas-software
docker compose down
```

Keep the `otas-takeoff-telemetry.yaml` recording if you need it for analysis;
remove or rename it yourself before a later run if you do not want to replace
it.

## Troubleshooting

- **Gazebo window does not appear:** Confirm Docker Desktop WSL integration is
  enabled for Ubuntu and WSLg is available. This GUI procedure is verified for
  Windows WSL 2, not macOS/XQuartz.
- **SITL does not detect `1:1`:** Confirm Gazebo is running with the
  `iris_runway.sdf` world and keep both Gazebo and SITL running.
- **MAVROS does not connect:** Wait for SITL's vehicle prompt, then check the
  launch command and `fcu_url` in Tab 4.
- **Telemetry does not report `OK`:** Confirm `/state` has `connected: true`
  and that Tab 5 includes the `/mavros/state:=/state` remap.
- **`telemetry_publisher` is not found:** Rebuild the workspace and source
  `/workspace/install/setup.bash` in the telemetry and echo commands.
- **Git reports an unsafe repository:** Run the Tab 1 `safe.directory` command
  inside the container.

Inside the container, run the ROS integration tests from `/workspace` after
sourcing ROS and the built workspace:

```bash
cd /workspace
source /opt/ros/humble/setup.bash
source install/setup.bash
pytest tests/
```
