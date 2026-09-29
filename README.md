# Autolabor Qt 操作界面与设计

从当前 Jetson AGX Orin 项目提取的 **Qt5 Widgets + ROS Noetic + 嵌入式 RViz** 操作界面，包含综合、GPS、远程、测试、视觉、清扫、日志七个页面，以及 ZED 原生参数面板。

本仓库提供界面源码、样式、截图、界面调用的辅助脚本及编译所需的 ROS 消息定义。导航规划、车辆控制、GNSS/雷达/相机驱动、YOLO 推理和模型均由外部项目提供。本仓库不启动这些后台模块。

![综合页（实际控件离线截图）](docs/screenshots/01_overview.png)

## 设计与源码入口

- [界面设计说明、配色与七页截图](design/README.md)
- [ROS 接口与外部模块对接](docs/ROS_INTERFACES.md)
- [提取范围及实际验证记录](docs/EXPORT_NOTES.md)
- [源码来源与 SHA-256 清单](docs/source_manifest.json)
- [主窗口与页面布局](src/application/autolabor_operator_gui/src/main_window.cpp)
- [清扫面板](src/application/autolabor_operator_gui/src/sweep_panel.cpp)、[ZED 参数面板](src/application/autolabor_operator_gui/src/zed_camera_panel.cpp)
- [全局 QSS 样式参考](design/theme.qss)

页面由 C++ 创建，样式在代码中设置，原项目没有 Qt Designer `.ui` 文件。`design/theme.qss` 是当前全局样式的提取副本；修改界面时以 C++ 中的样式为准。

## 编译

基准环境：Ubuntu 20.04、ROS Noetic、Qt 5、C++14。已在 Jetson AGX Orin ARM64 编译验证。界面本身不依赖 CUDA、TensorRT、ZED SDK 或海康 MVS SDK，但仍需要 ROS 和 RViz 开发库。

在已经配置 ROS Noetic 软件源的系统上安装依赖：

```bash
sudo apt update
sudo apt install build-essential cmake qtbase5-dev fonts-noto-cjk python3-nose \
  ros-noetic-catkin ros-noetic-roscpp ros-noetic-roslib ros-noetic-rviz \
  ros-noetic-actionlib-msgs ros-noetic-diagnostic-msgs \
  ros-noetic-dynamic-reconfigure ros-noetic-geometry-msgs ros-noetic-nav-msgs \
  ros-noetic-sensor-msgs ros-noetic-std-msgs ros-noetic-std-srvs \
  ros-noetic-message-generation ros-noetic-message-runtime \
  ros-noetic-rostest ros-noetic-roslaunch ros-noetic-rosbag

git clone git@github.com:Doribelove/QT-UI.git
cd QT-UI
./scripts/build_ui.sh -DCMAKE_BUILD_TYPE=Release
```

源码和所有接口定义均直接包含在仓库内，无需初始化子模块。构建脚本使用基础 ROS 环境，不依赖完整导航工作区。

## 打开与关闭界面

在有桌面显示的终端中：

```bash
cd ~/QT-UI
export ROS_MASTER_URI=http://127.0.0.1:11311
unset ROS_IP ROS_HOSTNAME
./scripts/operator_gui.sh
```

启动入口只启动 Qt 节点；没有 ROS master 时由 roslaunch 创建 master。没有业务后台时，界面会显示离线或等待状态。关闭窗口或在启动终端按 `Ctrl+C` 即可退出本次界面进程；此入口不负责关闭外部导航。

可选参数：

```bash
# 不显示嵌入式 RViz，适合不具备 OpenGL 显示环境的情况
./scripts/operator_gui.sh enable_rviz:=false

# 默认打开 ZED 参数面板，也可选海康面板
./scripts/operator_gui.sh camera_driver:=zed
./scripts/operator_gui.sh camera_driver:=hikrobot
```

连接已有机器人后台时，使用同一 ROS master，并确保双方 ROS 网络互通。GPS 目标、视觉回收、相机设置等按钮调用原有后台接口，其执行逻辑不在本仓库。清扫页保留原 TCP 辅助脚本，默认地址为 `192.168.0.197:50003`；界面启动后会查询一次状态，清扫页可见时每 5 秒查询。

## 离线设计截图与测试

```bash
# 从实际 Qt 控件生成全部七页截图，无需桌面显示或业务后台
./scripts/capture_ui.sh

source /opt/ros/noetic/setup.bash
source devel/setup.bash
export ROS_MASTER_URI=http://127.0.0.1:11395
unset ROS_IP ROS_HOSTNAME
catkin_make run_tests_autolabor_operator_gui -j2 -l2
(cd build && QT_QPA_PLATFORM=offscreen ctest -R operator_sweep_panel --output-on-failure)
catkin_test_results build/test_results
```

截图程序使用独立的无服务本机端点，并将清扫查询地址改成本机端点；不连接实车设备。截图中的离线提示是实际界面状态，地图与相机区域没有填入模拟实景。面板测试使用本机 TCP/ROS 模拟服务。

## 目录

```text
src/application/autolabor_operator_gui/   Qt 窗口、面板、RViz 配置及测试
src/application/autolabor_operator_msgs/ 远程目标及状态消息
src/application/autolabor_fod_msgs/      FOD 消息定义
src/interfaces/                         CAN 消息、海康相机服务定义（无驱动）
src/SweepDeviceControl/                  清扫通信类与测试辅助
scripts/                                界面启动、构建、截图、录包、清扫调用
tools/                                  实际 Qt 控件截图工具
design/                                 页面设计说明及 QSS 参考
docs/                                   截图、接口、来源与验证记录
```

`src/interfaces/` 保留原 ROS 包名和消息内容以兼容已有后台。请把本仓库作为独立工作区使用，避免将这些同名接口包复制进已有完整导航工作区。
