Gazebo Classic Dual Arms Setup

Overview

This repository documents the process of setting up and simulating a dual-arm robot in Gazebo Classic (Gazebo 11) with ROS 2 Humble. The URDF was exported from SolidWorks and adapted for ROS 2 control integration. The main goal was to achieve a stable simulation environment where the robot loads correctly, controllers can be applied, and Gazebo no longer crashes.

Problems Encountered

Apt Key Errors: Initially, the OSRF repository key was missing, causing NO_PUBKEY errors during apt update.

Plugin Crashes: The URDF contained both <ros2_control> and <gazebo> plugin blocks loading libgazebo_ros2_control.so. This duplication caused Gazebo to crash with exit code 255.

World File Missing: Gazebo attempted to load my_empty_world.world but the file did not exist, forcing a fallback to the default empty.world.

Ignition/Fortress Conflict: The system had Ignition/Fortress installed alongside Gazebo Classic, leading to mismatched plugin expectations and instability.

Solutions Implemented

Fixed Apt Key: Imported the OSRF GPG key and exported it to /etc/apt/keyrings/gazebo.gpg, resolving signature verification errors.

Removed Ignition/Fortress: Purged Ignition Gazebo packages to avoid conflicts and standardized on Gazebo Classic.

Simplified URDF: Removed duplicate <gazebo> plugin block and outdated <transmission> tags. Kept only the <ros2_control> block with gazebo_ros2_control/GazeboSystem plugin.

Created Custom World File: Added my_empty_world.world with ground plane, sun, and ROS plugins (gazebo_ros_state, gazebo_link_attacher). This ensures services like /get_entity_state are available.

Improved Launch File: Updated gazebo.launch.py to:

Process xacro → URDF.

Spawn the robot entity.

Load Gazebo with either my_empty_world.world or fallback to empty.world if missing.

Current Status

Gazebo Classic loads the URDF without crashing.

The robot entity spawns successfully.

Custom world file provides ROS services and a stable environment.

Next Steps

Extend URDF macros to support dual arms with prefixes (left_, right_).

Update <ros2_control> block to include both sets of joints.

Add ros2_controllers.yaml with two trajectory controllers (left and right arms).

Test trajectory execution and integrate with MoveIt2.

Usage

colcon build
source install/setup.bash
ros2 launch fairino_description gazebo.launch.py

Notes

Ensure gazebo_ros_pkgs is installed for ROS 2 integration.

Place custom world files in fairino_description/worlds/.

Controllers must be spawned after robot entity is loaded:

ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner left_arm_controller
ros2 run controller_manager spawner right_arm_controller