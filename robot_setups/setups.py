import os
import time
import pybullet as p
import pybullet_industrial as pi
import numpy as np


def setup_robot_by_type(robot_type):
    if robot_type == "Scara Robot":
        return setup_scaraRobot
    elif robot_type == "Gantry Robot":
        return setup_gantryRobot
    elif robot_type == "Articulated Robot":
        return setup_articulatedRobot
    else:
        raise ValueError("Unsupported robot type: " + robot_type)


def setup_scaraRobot():
    urdf_file = "C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/scaraRobot.urdf"

    start_orientation = p.getQuaternionFromEuler ([0, 0, 0])
    robot = pi.RobotBase(urdf_file, [0, 0, 0], start_orientation, 'end_effector')
    return(robot)

def setup_gantryRobot():
    urdf_file = "C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/gantryRobot.urdf"
    start_orientation = p.getQuaternionFromEuler ([0, 0, 0])
    robot = pi.RobotBase(urdf_file, [0, 0, 0], start_orientation, 'end_effector')
    return(robot)


def setup_articulatedRobot():
    urdf_file = "C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/articulatedRobot2.urdf"
    start_orientation = p.getQuaternionFromEuler ([0, 0, 0])
    robot = pi.RobotBase(urdf_file, [0, 0, 0], start_orientation, 'end_effector')
    return(robot)
