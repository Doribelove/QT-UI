# Qt 与后台接口

方向以 Qt 为基准。界面保留当前项目接口名称；本仓库仅实现界面及清扫 TCP 调用。

## 读取

| Topic | 用途 |
| --- | --- |
| `/gps/fix`、`/gps/heading`、`/gps/odom` | GNSS 经纬度、双天线航向和局部里程计 |
| `/gps/static_error/{current,rms,max,std_x,std_y,summary}` | 静态误差数据显示 |
| `/canbus_msg`、`/scan`、`/move_base/status` | CAN、雷达、导航状态 |
| `/rabbitmq_bridge/status`、`/rabbitmq_bridge/latest_target` | 消息队列状态及缓存目标 |
| `/fod_camera/image_raw`、`/fod/debug/image`、`/fod/detections` | 原始画面、检测画面及检测框信息 |
| `/fod_navigation_mode/{state,status}` | GPS/视觉回收模式 |
| `/fod_visual_servo/{state,status}` | 视觉回收进度与原因 |
| `/diagnostics` | 模块诊断 |
| `/zed2/zed_node/parameter_updates` | ZED 原生动态参数 |

嵌入式 RViz 还读取配置中的 TF、地图、轨迹和点云等 topic。默认 Fixed Frame 为 `camera_init`，具体配置见 `config/*.rviz`。

## 发布与服务调用

| Topic / Service | 类型或行为 |
| --- | --- |
| `/gps/goal_fix` | `sensor_msgs/NavSatFix`，WGS84 导航目标 |
| `/move_base_simple/goal` | RViz `2D Nav Goal` 工具，局部地图目标 |
| `/move_base/cancel` | `actionlib_msgs/GoalID`，取消导航 |
| `/gps/static_error/reset` | `std_msgs/Empty`，重置静态误差统计 |
| `/rabbitmq_bridge/publish_latest`、`/rabbitmq_bridge/clear_latest` | `std_srvs/Trigger` |
| `/fod_navigation_mode/set_fod_enabled` | `std_srvs/SetBool`，请求或取消一次回收 |
| `/fod_camera/driver/get_imaging_controls` | `hikrobot_mvs_camera/GetImagingControls` |
| `/fod_camera/driver/set_imaging_controls` | `hikrobot_mvs_camera/SetImagingControls` |
| `/fod_image_quality_controller/set_enabled` | `std_srvs/SetBool` |
| `/zed2/zed_node/set_parameters` | `dynamic_reconfigure/Reconfigure` |

Qt 不直接发布 `/cmd_vel`。回收距离、轨迹规划、速度、视觉目标选择等均由原后台实现。按钮是否可用保留当前界面判定逻辑，缺少后台时显示相应状态。

## 本地辅助程序

清扫页通过 `QProcess` 调用 `scripts/sweep_test.py --json`，使用 `src/SweepDeviceControl/SweepDeviceControl.py` 与设备 TCP 通信，保留原操作锁及异步交互。录包按钮调用 `scripts/record_rosbag.sh`，生成的日志和 rosbag 已加入 `.gitignore`。

## 编译用接口包

- `autolabor_operator_msgs`：远程目标与 RabbitMQ 状态定义。
- `autolabor_fod_msgs`：原 FOD 消息定义，未包含检测、投影、跟踪算法。
- `autolabor_canbus_driver`：只含原 `CanBusMessage.msg`。
- `hikrobot_mvs_camera`：只含原 `GetImagingControls.srv` 与 `SetImagingControls.srv`。

后两个包位于 `src/interfaces/`，保留原 ROS 包名及消息内容以保持线上的类型兼容性，不包含 CAN 驱动、海康驱动或厂商 SDK。此工作区应单独编译，通过 ROS 网络连接完整系统；不要将同名接口包加入已有完整工作区。
