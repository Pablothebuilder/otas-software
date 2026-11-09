# OTAS Software Team Coding Standards

## 1. Python Standards
* **Style Guide:** Follow PEP 8.
* **Linter:** All Python files must pass `flake8` checks clean before merging[cite: 3].
* **Naming Conventions:**
  * Modules & files: `snake_case.py`
  * Classes: `PascalCase`
  * Functions & variables: `snake_case`
* **ROS 2 Nodes:** Always include explicit type hints for ROS 2 node publishers, subscribers, and service calls[cite: 2].

## 2. C++ Standards
* **Standard:** C++17[cite: 2].
* **Linter:** Code must comply with `cpplint` rules[cite: 3].
* **Naming Conventions:**
  * Files: `snake_case.cpp` / `snake_case.hpp`
  * Classes: `PascalCase`
  * Member variables: `m_variable_name` or `variable_name_`

## 3. ROS 2 & MAVLink Naming Conventions
* **Topics & Services:** `snake_case` (e.g., `/otas/telemetry/1hz_out`, `/otas/safety/terminate`)[cite: 2, 3].
* **Custom Messages & Interfaces:** `PascalCase` (e.g., `TelemetryPacket.msg`).
* **Telemetry Requirements:** Telemetry nodes must output fields at 1 Hz adhering strictly to AEAC specification fields[cite: 2, 3].

## 4. Git Commit Messages
Use Conventional Commit formatting:
* `feat:` A new feature (e.g., `feat: implement T5 telemetry 1Hz publisher`)[cite: 2, 3]
* `fix:` A bug fix (e.g., `fix: resolve heartbeat link-loss timeout in T2`)[cite: 3]
* `docs:` Documentation changes (e.g., `docs: add setup instructions for Gazebo Harmonic`)
* `test:` Adding or modifying test scripts (e.g., `test: add T3 geofence boundary test`)[cite: 3]
