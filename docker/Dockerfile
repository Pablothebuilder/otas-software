FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV PATH="/usr/local/bin:${PATH}"

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
    ros-humble-mavros-msgs \
    gz-harmonic \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# 4. Install ArduPilot Tools & MAVProxy
RUN pip3 install --no-cache-dir \
    pymavlink \
    MAVProxy \
    cpplint

# 5. Install Linters Explicitly via APT
RUN apt-get update && apt-get install -y \
    flake8 \
    python3-pytest \
    && ln -s /usr/bin/pytest-3 /usr/bin/pytest

# 6. Set Workspace Environment
WORKDIR /workspace
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["/bin/bash"]
