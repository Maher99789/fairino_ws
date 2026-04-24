Dual Arms URDF Loads but Invisible in Gazebo

1/Environment

ROS 2 Distribution: Humble

Gazebo Version: Fortress v6.17.1

Workspace: ~/fairino_ws

Package: fairino_description



2/Problem Summary

When launching the dual-arm robot URDF in Gazebo, the process completes successfully:

robot_state_publisher reports all segments (floor_link, left/right arms, wrists, etc.).

spawn_entity.py confirms: Successfully spawned entity [fairino_dual_arms].

robot_description parameter is present in robot_state_publisher.

Despite this, the robot does not appear visually in the Gazebo environment. Gazebo opens, but the dual arms are invisible.

3/Logs

Launch Output

terminal1:~/fairino_ws$ ros2 launch fairino_description gazebo.launch.py
[INFO] [launch]: All log files can be found below /home/souey-maher/.ros/log/2026-04-24-17-54-38-608507-Souey-Maher-95144
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [gzserver-1]: process started with pid [95145]
[INFO] [gzclient-2]: process started with pid [95147]
[INFO] [robot_state_publisher-3]: process started with pid [95149]
[INFO] [spawn_entity.py-4]: process started with pid [95151]
[robot_state_publisher-3] [INFO] [1777049679.036459269] [robot_state_publisher]: got segment floor_link
[robot_state_publisher-3] [INFO] [1777049679.036594999] [robot_state_publisher]: got segment left_base_link
[robot_state_publisher-3] [INFO] [1777049679.036599708] [robot_state_publisher]: got segment left_forearm_link
[robot_state_publisher-3] [INFO] [1777049679.036602462] [robot_state_publisher]: got segment left_shoulder_link
[robot_state_publisher-3] [INFO] [1777049679.036604901] [robot_state_publisher]: got segment left_upperarm_link
[robot_state_publisher-3] [INFO] [1777049679.036607222] [robot_state_publisher]: got segment left_wrist1_link
[robot_state_publisher-3] [INFO] [1777049679.036609490] [robot_state_publisher]: got segment left_wrist2_link
[robot_state_publisher-3] [INFO] [1777049679.036611617] [robot_state_publisher]: got segment left_wrist3_link
[robot_state_publisher-3] [INFO] [1777049679.036613631] [robot_state_publisher]: got segment right_base_link
[robot_state_publisher-3] [INFO] [1777049679.036615759] [robot_state_publisher]: got segment right_forearm_link
[robot_state_publisher-3] [INFO] [1777049679.036618080] [robot_state_publisher]: got segment right_shoulder_link
[robot_state_publisher-3] [INFO] [1777049679.036620202] [robot_state_publisher]: got segment right_upperarm_link
[robot_state_publisher-3] [INFO] [1777049679.036622407] [robot_state_publisher]: got segment right_wrist1_link
[robot_state_publisher-3] [INFO] [1777049679.036624399] [robot_state_publisher]: got segment right_wrist2_link
[robot_state_publisher-3] [INFO] [1777049679.036626396] [robot_state_publisher]: got segment right_wrist3_link
[robot_state_publisher-3] [INFO] [1777049679.036628406] [robot_state_publisher]: got segment world
[spawn_entity.py-4] [INFO] [1777049679.638632986] [spawn_entity]: Spawn Entity started
[spawn_entity.py-4] [INFO] [1777049679.638837510] [spawn_entity]: Loading entity published on topic robot_description
[spawn_entity.py-4] [INFO] [1777049679.645197509] [spawn_entity]: Waiting for entity xml on robot_description
[spawn_entity.py-4] [INFO] [1777049679.656734103] [spawn_entity]: Waiting for service /spawn_entity, timeout = 30
[spawn_entity.py-4] [INFO] [1777049679.657000927] [spawn_entity]: Waiting for service /spawn_entity
[spawn_entity.py-4] [INFO] [1777049680.169412861] [spawn_entity]: Calling service /spawn_entity
[spawn_entity.py-4] [INFO] [1777049680.415624666] [spawn_entity]: Spawn status: SpawnEntity: Successfully spawned entity [fairino_dual_arms]
[INFO] [spawn_entity.py-4]: process has finished cleanly [pid 95151]

Parameter Check

terminal2:~/fairino_ws$ ros2 param list /robot_state_publisher
  frame_prefix
  ignore_timestamp
  publish_frequency
  qos_overrides./joint_states.subscription.depth
  qos_overrides./joint_states.subscription.history
  qos_overrides./joint_states.subscription.reliability
  qos_overrides./parameter_events.publisher.depth
  qos_overrides./parameter_events.publisher.durability
  qos_overrides./parameter_events.publisher.history
  qos_overrides./parameter_events.publisher.reliability
  qos_overrides./tf.publisher.depth
  qos_overrides./tf.publisher.durability
  qos_overrides./tf.publisher.history
  qos_overrides./tf.publisher.reliability
  qos_overrides./tf_static.publisher.depth
  qos_overrides./tf_static.publisher.history
  qos_overrides./tf_static.publisher.reliability
  robot_description
  use_sim_time

This confirms the URDF is loaded.

4/Test with Box URDF

To isolate the issue, a simple box URDF (test_box.urdf.xacro) was launched:

ros2 launch fairino_description gazebo.launch.py urdf_file:=test_box.urdf.xacro

Gazebo loaded instantly.

The box appeared correctly.

This proves the URDF pipeline and Gazebo setup are correct. The problem is specific to the robot meshes.

5/Likely Causes

Mesh format issues

STL files may be binary or malformed.

DAE exports may lack triangulation or transforms.

Scale mismatch

CAD exports often use millimeters, while Gazebo expects meters.

Robot may be microscopic or gigantic, appearing outside the camera view.

Origin offset

Mesh geometry may be far from (0,0,0), spawning outside the visible area.

High polygon count

Large STL meshes slow Gazebo startup and may fail to render.

6/Current Status

URDF loads successfully.

Entity spawns successfully.

Box URDF test passes.

Dual-arm robot meshes fail to render.

7/Conclusion

The URDF and launch pipeline are correct. The invisibility issue is caused by mesh problems (format, scale, or complexity). Re-exporting and simplifying meshes with correct transforms is required to resolve the problem.

Note: This document is intended for GitHub issue tracking. The solution is not yet found. The box URDF test confirms the pipeline works, but the dual-arm robot remains invisible in Gazebo due to mesh issues.