# Autolabor Qt 操作台

当前项目的 Qt5 Widgets / ROS Noetic / librviz 界面，包含综合、GPS、远程、测试、视觉、清扫和日志页面，以及 ZED 原生参数面板。

这是独立 Qt 提取仓库中的界面包。完整的依赖安装、编译、启动和测试方法见[仓库说明](../../../README.md)，页面截图与样式见[设计说明](../../../design/README.md)，后台对接见[接口说明](../../../docs/ROS_INTERFACES.md)。

在仓库根目录运行：

```bash
./scripts/build_ui.sh -DCMAKE_BUILD_TYPE=Release
./scripts/operator_gui.sh
```

`operator_gui.launch` 仅启动界面；参数为 `enable_rviz`、`camera_driver` 和 `rviz_config`。ROS master 或可选业务节点缺失时，界面仍可打开并显示离线状态。界面通过既有 topic/service 与后台交互，不直接发布 `/cmd_vel`。

页面由 `src/main_window.cpp` 创建，无独立 `.ui` 文件。清扫页调用仓库中的 TCP 辅助脚本；相机设置通过原 ROS 服务调用外部相机节点。
