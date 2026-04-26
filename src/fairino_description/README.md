Dual Arm Robot Simulation – ROS 2 Humble
Overview

This workspace (fairino_ws) integrates a dual-arm robot into Gazebo using ROS 2 Humble.
Controllers are managed via ros2_control and controller_manager.
Installation

Clone the repository and build:
bash

cd ~/fairino_ws
colcon build
source install/setup.bash

Ensure the following packages are installed:

    ros-humble-ros2-control

    ros-humble-ros2-controllers

    ros-humble-controller-manager

    ros-humble-position-controllers

    ros-humble-joint-state-broadcaster

Check with:
bash

apt list --installed | grep ros-humble

Launch Simulation

Start Gazebo with the dual-arm robot:
bash

ros2 launch fairino_description gazebo.launch.py

Controller Spawning

Spawn controllers manually:
bash

ros2 run controller_manager spawner joint_state_broadcaster --controller-manager /controller_manager
ros2 run controller_manager spawner dual_arm_position_controller --controller-manager /controller_manager

Example Output
text

[INFO] [spawner_joint_state_broadcaster]: Loaded joint_state_broadcaster
[INFO] [spawner_joint_state_broadcaster]: Configured and activated joint_state_broadcaster
[INFO] [spawner_dual_arm_position_controller]: Loaded dual_arm_position_controller
[ERROR] [spawner_dual_arm_position_controller]: Failed to configure controller

Listing controllers:
bash

ros2 control list_controllers

Result:
text

joint_state_broadcaster      joint_state_broadcaster/JointStateBroadcaster      active
dual_arm_position_controller position_controllers/JointGroupPositionController  unconfigured

Problem Explanation

    The dual_arm_position_controller loads but remains unconfigured.

    This indicates the plugin is found, but it cannot bind to the hardware interfaces.

    Root cause: URDF <ros2_control> block syntax.
    In ROS 2 Humble, each joint must declare interfaces using plural tags:

xml

<command_interfaces>
  <position/>
</command_interfaces>
<state_interfaces>
  <position/>
</state_interfaces>

If singular tags (<command_interface name="position"/>) are used, the controller loads but fails to configure.