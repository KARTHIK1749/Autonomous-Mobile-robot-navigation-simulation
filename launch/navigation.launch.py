
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import SetRemap
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    package_share = FindPackageShare("mobile_robot")

    map_file = PathJoinSubstitution([
        package_share,
        "maps",
        "maze_map_save.yaml",
    ])

    nav2_params = PathJoinSubstitution([
        package_share,
        "config",
        "nav2_params.yaml",
    ])

    nav2 = GroupAction([
        # Route Nav2's controller output to a separate topic.
        SetRemap(src="cmd_vel", dst="/cmd_vel_nav"),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare("nav2_bringup"),
                    "launch",
                    "bringup_launch.py",
                ])
            ),
            launch_arguments={
                "map": map_file,
                "params_file": nav2_params,
                "use_sim_time": "True",
                "autostart": "True",
                "slam": "False",
                "use_composition": "False",
            }.items(),
        ),
    ])

    return LaunchDescription([nav2])
