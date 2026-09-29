#!/usr/bin/env bash
set -euo pipefail
UI_WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/noetic/setup.bash
source "$UI_WS/devel/setup.bash"
export QT_QPA_PLATFORM=offscreen
exec "$UI_WS/devel/lib/autolabor_operator_gui/qt_ui_capture" \
  "${1:-$UI_WS/docs/screenshots}"
