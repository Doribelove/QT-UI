# Qt 提取与验证记录

日期：2026-09-29。

来源：[Doribelove/autolabor-robot-nav](https://github.com/Doribelove/autolabor-robot-nav)，提交 `4e1117cd3c8892cc48b29e3beeb5a85679921930`，对应 Jetson 上当前 `/home/slam/robot_ws_agx` 工作区。

目标：[Doribelove/QT-UI](https://github.com/Doribelove/QT-UI)，`main` 分支。提取、构建和测试均在独立目录 `/home/slam/QT-UI` 完成。

## 保留内容

- Qt 主窗口、七个页面、清扫面板、ZED 原生参数面板的全部 C++ 源码与头文件，逐文件保持与来源一致。
- 当前 RViz 显示配置、Qt 原有界面测试。
- 界面直接使用的启动、录包、清扫辅助脚本，以及清扫通信类和本机测试辅助程序。
- 原 FOD/操作台消息定义；CAN 与海康只提取界面所需消息/服务定义。

未纳入导航控制、规划、定位、传感器驱动实现、YOLO 算法/模型、厂商 SDK、完整启动脚本、录包、日志、编译结果或原仓库历史。GitHub 首次提交只包含本次 Qt 提取内容。

## 为独立工作区所做的适配

1. 提供 catkin 顶层构建文件、构建脚本及两个仅含接口定义的包，保持原 ROS 类型名称与内容。
2. Qt launch 仅启动界面，移除完整系统的 GPS 误差监控节点 include；Qt 包声明也移除对应后台依赖。
3. 保留五项 Qt 接口契约测试，移除两项只验证完整导航启动脚本的测试。
4. 录包脚本缺少 ROS master 时的提示改为连接外部 master，不再指向本仓库未提供的完整启动脚本。
5. 添加实际控件离线截图工具、设计文档、QSS 参考、界面接口与使用说明。

源码来源及提取后哈希见 [source_manifest.json](source_manifest.json)。`identical_to_source` 标明复制文件是否保持原字节内容；界面 C++、头文件、RViz 配置及所有消息/服务定义均保持一致。

## 实际验证结果

环境：Jetson AGX Orin、ARM64/aarch64、Ubuntu 20.04.6、ROS Noetic、Qt 5.12.8。

| 验证 | 结果 |
| --- | --- |
| 独立 Release 构建 | 通过；仅使用 `/opt/ros/noetic` 基础工作区，构建 5 个 catkin 包 |
| GUI 接口契约 | 5 项通过 |
| ZED 面板模拟服务 | 5 项功能测试通过，覆盖读取、手动应用、自动模式、服务缺失、参数不完整；QtTest 含初始化/清理共 7 项 |
| catkin 结果汇总 | 13 项、0 错误、0 失败、0 跳过（包含框架用例） |
| 清扫面板模拟 TCP | 3 项功能测试通过，覆盖按钮与响应、启动过程中排队停止、通信失败重试；QtTest 含初始化/清理共 5 项 |
| 实际窗口离线渲染 | 七页 PNG 成功生成，综合/视觉/清扫截图已检查 |

验证使用独立 ROS 测试 master、本机模拟服务和离线截图程序；没有启动完整导航、调用实车运动、访问真实清扫设备或修改原导航项目。截图使用 `127.0.0.1:1` 作为无服务端点，因此出现离线/查询失败提示属于预期。

RViz 链接和配置随界面构建通过；本次没有使用真实地图、相机流或整车运动验证，也没有把离线截图作为这些后台功能的验收。

本机构建和测试原始输出保留在 `log/build_ui.log`、`log/test_ui.log`、`log/capture_ui.log`、`build/test_results/` 和 `build/Testing/Temporary/LastTest.log`，不上传生成文件。
