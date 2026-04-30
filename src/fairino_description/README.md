fairino_description
Overview

This package contains the description, configuration, and launch files for simulating and visualizing the dual‑arm Fairino robot. It supports:

    Visualization in RViz

    Simulation in Gazebo

    Initialization of joint positions from YAML configuration

    Integration with ROS 2 controllers for dual‑arm control

Features

    RViz Visualization: Load the robot model and interactively control joints.

    Gazebo Simulation: Spawn the robot into Gazebo for physics‑based simulation.

    Initial Positions: Load joint states from config/initial_positions.yaml to start with a defined pose.

    Controller Integration: Use ROS 2 control to manage joint state broadcaster and dual‑arm position controllers.

Problems Encountered and Solutions

    RViz not showing robot model

        Cause: robot_description parameter not set correctly.

        Solution: Changed RViz RobotModel Description Source from Topic to Parameter and set parameter name to robot_description.

    Gazebo crash under ros2_controller

        Cause: Plugin misconfiguration and Ignition/Fortress conflicts.

        Solution: Removed Ignition/Fortress Gazebo, installed Gazebo Classic, and corrected YAML controller configuration.

    Launch file errors with initial_pose_publisher

        Cause: Executable not registered in setup.py.

        Solution: Added entry point in setup.py and rebuilt package.

    Dual‑arm controllers not initializing correctly

        Cause: Missing initial joint positions.

        Solution: Added explicit zeros in initial_positions.yaml under joint_state_publisher_gui.

yaml

joint_state_publisher_gui:
  ros__parameters:
    zeros:
      left_joint1: -1.57
      left_joint2: -1.57
      left_joint3:  1.57
      left_joint4:  0.0
      left_joint5:  3.14
      left_joint6:  0.0
      right_joint1:  1.57
      right_joint2: -1.57
      right_joint3: -1.57
      right_joint4:  3.14
      right_joint5:  3.14
      right_joint6:  0.0

This fixed initialization and allowed both RViz and Gazebo to load the robot with the correct starting pose.
Debugging Commands Used
bash

# Inspect nodes and topics
ros2 node list
ros2 topic list

# Spawn joint state broadcaster
ros2 run controller_manager spawner joint_state_broadcaster --controller-manager /controller_manager

# Spawn dual-arm position controller
ros2 run controller_manager spawner dual_arm_position_controller --controller-manager /controller_manager

# Verify hardware interfaces
ros2 control list_hardware_interfaces

# Launch RViz with description
ros2 launch fairino_description display.launch.py

# Launch Gazebo with robot
ros2 launch fairino_description gazebo.launch.py

# Run pose publisher directly
ros2 run fairino_description dual_arm_mover.py