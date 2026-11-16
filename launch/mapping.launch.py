
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    package_share = FindPackageShare("mobile_robot")

    slam_params = PathJoinSubstitution([
        package_share,
        "config",
        "slam_mapping_params.yaml",
    ])

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("slam_toolbox"),
                "launch",
                "online_async_launch.py",
            ])
        ),
        launch_arguments={
            "slam_params_file": slam_params,
            "use_sim_time": "true",
        }.items(),
    )

    return LaunchDescription([slam])
