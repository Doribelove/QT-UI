cmake_minimum_required(VERSION 3.0.2)
project(autolabor_canbus_driver)
# UI-only wire definitions; no hardware driver or vendor SDK is built.
find_package(catkin REQUIRED COMPONENTS message_generation std_msgs)
add_message_files(FILES CanBusMessage.msg)
generate_messages(DEPENDENCIES std_msgs)
catkin_package(CATKIN_DEPENDS message_runtime std_msgs)
