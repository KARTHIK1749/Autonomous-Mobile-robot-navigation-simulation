#!/usr/bin/env python3

import math
import subprocess

import rclpy
from rclpy.node import Node
from rclpy.time import Time

from tf2_ros import Buffer, TransformListener, TransformException


class LidarVisualizerFix(Node):

    def __init__(self):
        super().__init__('lidar_visualizer_fix')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(
            self.tf_buffer,
            self
        )

        self.initial_x = None
        self.initial_y = None

        self.fix_executed = False
        self.waiting_message_printed = False

        self.timer = self.create_timer(
            0.2,
            self.check_robot_motion
        )

        self.get_logger().info(
            'Waiting for TF odom -> lidar_link...'
        )

    def check_robot_motion(self):

        if self.fix_executed:
            return

        try:
            transform = self.tf_buffer.lookup_transform(
                'odom',
                'lidar_link',
                Time()
            )

        except TransformException:

            if not self.waiting_message_printed:
                self.get_logger().info(
                    'TF odom -> lidar_link not available yet...'
                )
                self.waiting_message_printed = True

            return

        x = transform.transform.translation.x
        y = transform.transform.translation.y

        if self.initial_x is None:

            self.initial_x = x
            self.initial_y = y

            self.get_logger().info(
                f'Initial LiDAR position detected: '
                f'x={x:.3f}, y={y:.3f}'
            )

            self.get_logger().info(
                'Waiting for robot movement...'
            )

            return

        distance = math.sqrt(
            (x - self.initial_x) ** 2 +
            (y - self.initial_y) ** 2
        )

        if distance >= 0.02:

            self.get_logger().info(
                f'Robot movement detected: '
                f'{distance:.3f} m'
            )

            self.execute_fix()

    def execute_fix(self):

        self.fix_executed = True

        self.get_logger().info(
            'Executing Gazebo LiDAR visualization workaround...'
        )

        command = [
            'gz',
            'model',
            '-m',
            'mobile_robot',
            '-l',
            'lidar_link'
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:

                self.get_logger().info(
                    'Gazebo LiDAR visualization synchronized successfully.'
                )

            else:

                self.get_logger().error(
                    'gz model command failed.'
                )

                if result.stderr:
                    self.get_logger().error(result.stderr)

        except Exception as e:

            self.get_logger().error(
                f'Error while executing workaround: {e}'
            )

        self.get_logger().info(
            'LiDAR workaround completed. Node will stop.'
        )

        self.timer.cancel()

        self.create_timer(
            0.5,
            self.shutdown_node
        )

    def shutdown_node(self):

        if rclpy.ok():
            rclpy.shutdown()


def main(args=None):

    rclpy.init(args=args)

    node = LidarVisualizerFix()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()