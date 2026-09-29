cmake_minimum_required(VERSION 3.0.2)
project(hikrobot_mvs_camera)
# UI-only wire definitions; no hardware driver or vendor SDK is built.
find_package(catkin REQUIRED COMPONENTS message_generation std_msgs)
add_service_files(FILES GetImagingControls.srv SetImagingControls.srv)
generate_messages(DEPENDENCIES std_msgs)
catkin_package(CATKIN_DEPENDS message_runtime std_msgs)
