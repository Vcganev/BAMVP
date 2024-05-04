import os
import time
import pybullet as p
import pybullet_industrial as pi
import numpy as np



#threshold = 0.02
#Setup scaraRobot
#target_positions = [[0, 3, 1], [3, 0, 1],[-3, 0, 1], [0, -3, 1] ]

def setup_scaraRobot():
    urdf_file = "C:/Users/victo/OneDrive/Dokumente/BA/Matlab/reachabilityExperiment/Ex_1_scaraRobot4/scaraRobot4.urdf"
    #physics_client = p.connect(p.DIRECT)
    #p.setRealTimeSimulation(1)
    #p.setPhysicsEngineParameter(numSolverIterations=1000)
    start_orientation = p.getQuaternionFromEuler ([0, 0, 0])
    robot = pi.RobotBase(urdf_file, [0, 0, 0], start_orientation, 'end_effector')
    return(robot)


#robot = setup_scaraRobot()
#for target_position in target_positions:
    robot.set_endeffector_pose(target_position)
    time.sleep(1)
    current_position, _ = robot.get_endeffector_pose('end_effector')
    distance = np.linalg.norm(current_position - target_position)
    if distance <= threshold:
            print("Point",target_position, "reached")
    else:
            print("Point",target_position, "not reached")
        # Sleep for a bit to visually inspect the simulation
    time.sleep(3)
    