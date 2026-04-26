import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('fairino_description')
    xacro_file = os.path.join(pkg_share, 'urdf_dual_arms', 'fairino3_dual_arms.urdf.xacro')

    # Process Xacro to URDF
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = robot_description_config.toxml()

    # Gazebo world
    world = os.path.join(pkg_share, 'worlds', 'my_empty_world.world')
    if not os.path.exists(world):
        world = '/usr/share/gazebo-11/worlds/empty.world'

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world}.items(),
    )

    # Robot State Publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    # Spawn entity in Gazebo
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'fairino_dual_arms', '-topic', 'robot_description'],
        output='screen'
    )

    return LaunchDescription([gazebo, rsp, spawn])
