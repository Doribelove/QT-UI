#!/usr/bin/env python3

from pathlib import Path
import unittest
import xml.etree.ElementTree as ElementTree


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PACKAGE_ROOT.parents[2]
GUI_SOURCE = (PACKAGE_ROOT / "src" / "main_window.cpp").read_text(encoding="utf-8")
GUI_HEADER = (
    PACKAGE_ROOT / "include" / "autolabor_operator_gui" / "main_window.h"
).read_text(encoding="utf-8")
RVIZ_CONFIG = (PACKAGE_ROOT / "config" / "operator_navigation.rviz").read_text(
    encoding="utf-8"
)


class OperatorGuiContractTest(unittest.TestCase):
    def test_embedded_rviz_has_2d_navigation_goal_tool(self):
        tools = RVIZ_CONFIG[RVIZ_CONFIG.index("  Tools:") :]
        self.assertIn("- Class: rviz/SetGoal", tools)
        set_goal = tools[tools.index("- Class: rviz/SetGoal") :]
        self.assertIn("Topic: /move_base_simple/goal", set_goal.split("Value:", 1)[0])
        self.assertIn("Fixed Frame: camera_init", RVIZ_CONFIG)

    def test_heading_and_manual_wgs84_goal_are_visible(self):
        self.assertIn('node_->subscribe("/gps/heading"', GUI_SOURCE)
        self.assertIn("北 0°，顺时针", GUI_SOURCE)
        self.assertIn("发送 GPS 目标点", GUI_SOURCE)
        self.assertIn('advertise<sensor_msgs::NavSatFix>("/gps/goal_fix"', GUI_SOURCE)
        self.assertIn("sendManualGpsGoal", GUI_HEADER)

    def test_camera_yolo_and_runtime_imaging_controls_are_integrated(self):
        for topic in (
            "/fod_camera/image_raw",
            "/fod/debug/image",
            "/fod/detections",
        ):
            self.assertIn(topic, GUI_SOURCE)
        self.assertIn("hikrobot_mvs_camera::GetImagingControls", GUI_SOURCE)
        self.assertIn("hikrobot_mvs_camera::SetImagingControls", GUI_SOURCE)
        self.assertIn("启动相机控制回收", GUI_SOURCE)

    def test_visual_motion_uses_safe_mode_arbiter_only(self):
        self.assertIn(
            '"/fod_navigation_mode/set_fod_enabled"',
            GUI_SOURCE,
        )
        self.assertNotIn('advertise<geometry_msgs::Twist>', GUI_SOURCE)
        self.assertNotIn('"/fod_visual_servo/set_enabled"', GUI_SOURCE)
        self.assertNotIn('advertise<', GUI_SOURCE.split("setupRosInterfaces", 1)[0])

    def test_manifest_declares_new_ros_interfaces(self):
        root = ElementTree.parse(str(PACKAGE_ROOT / "package.xml")).getroot()
        dependencies = {element.text for element in root.findall("depend")}
        self.assertTrue(
            {"autolabor_fod_msgs", "diagnostic_msgs", "hikrobot_mvs_camera"}
            <= dependencies
        )


if __name__ == "__main__":
    unittest.main()
