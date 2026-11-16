from launch import LaunchDescription ## it is like a container of contents to be launched
from launch_ros.actions import Node 
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription , SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource ## The launch file im including is a python file so we use this class to include it

from launch.substitutions import PathJoinSubstitution, Command ## Pathjoin substitution is used to join paths and command is used to run a command and get the output of it
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler, TimerAction, ExecuteProcess
from launch.event_handlers import OnProcessExit

## Step - 1 : Create a fxn to generate launch description

    ## Workaround: register the lidar link with Gazebo's GUI after spawning
    # register_lidar = RegisterEventHandler(
    #     OnProcessExit(
    #         target_action=spawn_robot,
    #         on_exit=[
    #             TimerAction(
    #                 period=3.0,
    #                 actions=[
    #                     ExecuteProcess(
    #                         # cmd=["gz", "model", "-m", "mobile_robot", "-l", "lidar_link"],
    #                         cmd = [ "gz","sim","-v","4","--model-info","mobile_robot", "--link","lidar_link"],
    #                         output="screen",
    #                     )
    #                 ],
    #             )
    #         ],
    #     )
    # )

def generate_launch_description():

    ## Find the path of package
    package_share = FindPackageShare("mobile_robot")

    ## find the path to xacro file 
    robot_xacro = PathJoinSubstitution([package_share, "model", "robot.xacro"])

    ## Path to Gazebo world
    world_file = PathJoinSubstitution(
        [package_share, "worlds", "maze_world.sdf"]
    )

    ## Convert xacro to urdf using a launch substitution
    robot_description = Command(['xacro ', robot_xacro])

    ## Start robot state publisher
    robot_state_publisher = Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        output = "screen",
        parameters = [{"robot_description": ParameterValue(robot_description, value_type=str), "use_sim_time": True}]
    )

    ## Gazebo GUI workaround for Hyprland / Wayland
    set_qt_platform = SetEnvironmentVariable(
        "QT_QPA_PLATFORM",
        "xcb"
    )

    ## Force Gazebo Transport to use localhost
    set_gz_ip = SetEnvironmentVariable(
        "GZ_IP",
        "127.0.0.1"
    )

    ## Start gazebo simulation
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"])),
        # launch_arguments = {"gz_args" : ["-r ", world_file]}.items()
        launch_arguments = {"gz_args" : ["-r ", world_file],'on_exit_shutdown': 'true'}.items()
    )
    

    ## Spawn robot in gazebo
    spawn_robot = Node(
         package = "ros_gz_sim",
         executable = "create",
         output = "screen",
         arguments = ["-topic", "robot_description", "-name", "mobile_robot","-x", "-4.0", "-y", "3.3", "-z", "0.2"]
    )


    ## Bridge the ros and gazebo topics
    bridge_configs = PathJoinSubstitution([package_share, "parameters", "build_params.yaml"])
    bridge = Node(
        package = "ros_gz_bridge",
        executable = "parameter_bridge",
        output = "screen",
        parameters = [{'config_file': bridge_configs}]
    )

    rviz_node = Node(
        package = "rviz2",
        executable = "rviz2",
        output = "screen",
        parameters = [{"use_sim_time": True}]
    )

    
    return LaunchDescription([
        set_qt_platform, set_gz_ip, gazebo, spawn_robot, robot_state_publisher, bridge , rviz_node
    ])
