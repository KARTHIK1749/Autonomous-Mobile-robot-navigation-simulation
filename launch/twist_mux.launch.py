
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    mux_config = PathJoinSubstitution([
        FindPackageShare("mobile_robot"),
        "config",
        "twist_mux.yaml",
    ])

    twist_mux_node = Node(
        package="twist_mux",
        executable="twist_mux",
        name="twist_mux",
        output="screen",
        parameters=[mux_config],
        remappings=[
            ("cmd_vel_out", "/cmd_vel"),
        ],
    )

    return LaunchDescription([
        twist_mux_node,
    ])
