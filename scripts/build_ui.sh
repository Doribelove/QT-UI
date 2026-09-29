#!/usr/bin/env bash
set -euo pipefail
UI_WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_SETUP="${ROS_SETUP:-/opt/ros/noetic/setup.bash}"
if [[ ! -f "$ROS_SETUP" ]]; then
  echo "Missing ROS Noetic environment: $ROS_SETUP" >&2
  exit 2
fi
# Build against the base ROS installation, not a full robot workspace overlay.
unset CMAKE_PREFIX_PATH ROS_PACKAGE_PATH ROSLISP_PACKAGE_DIRECTORIES
source "$ROS_SETUP"
cd "$UI_WS"
catkin_make -j2 -l2 -DPYTHON_EXECUTABLE=/usr/bin/python3 "$@"
