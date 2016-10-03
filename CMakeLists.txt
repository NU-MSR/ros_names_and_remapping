cmake_minimum_required(VERSION 2.8.3)
project(ros_names_and_remapping)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
  )

catkin_package(
  CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs
  )

# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)
