
from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mobile_robot'

setup(
    name=package_name,
    version='0.0.0',

    packages=find_packages(exclude=['test']),

    data_files=[
        # ament package index
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),

        # package.xml
        (
            'share/' + package_name,
            ['package.xml']
        ),

        # Launch files
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),

        # Robot description / Xacro / URDF
        (
            os.path.join('share', package_name, 'model'),
            glob('model/*')
        ),

        # ROS-Gazebo bridge parameters
        (
            os.path.join('share', package_name, 'parameters'),
            glob('parameters/*')
        ),

        # Gazebo worlds
        (
            os.path.join('share', package_name, 'worlds'),
            glob('worlds/*')
        ),

        # config files
        (
            os.path.join("share", package_name , "config"), glob("config/*")
        ),
        (
            os.path.join("share", package_name , "maps"), glob('maps/*')
        )
    ],

    install_requires=['setuptools'],

    zip_safe=True,

    maintainer='karthii',
    maintainer_email='karthii@todo.todo',

    description='Mobile robot simulation using ROS 2 Jazzy and Gazebo',

    license='TODO: License declaration',

    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={
    'console_scripts': [],
},
)