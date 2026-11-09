# OTAS Software Team Coding Standards
cat << 'EOF' > docker/Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

# 1. Base System Utilities & Locales
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    git \
    sudo \
    wget \
    python3-pip \
    python3-dev \
    locales \
    && locale-gen en_US en_US.UTF-8 \
    && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8

# 2. Add APT Repositories for ROS 2 Humble & Gazebo Harmonic
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" > /etc/apt/sources.list.d/ros2.list

RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" > /etc/apt/sources.list.d/gazebo-stable.list

# 3. Install ROS 2 Humble, Gazebo Harmonic & GZ ROS Bridge
RUN apt-get update && apt-get install -y \
    ros-humble-ros-base \
    ros-humble-ros-gzharmonic \
    gz-harmonic \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# 4. Install ArduPilot Tools, MAVProxy & Testing Frameworks
RUN pip3 install --no-cache-dir \
    pymavlink \
    MAVProxy \
    pytest \
    flake8 \
    cpplint

# 5. Set Workspace Environment
WORKDIR /workspace
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["/bin/bash"]
EOF
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
