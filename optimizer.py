import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pybullet as p
from rolap import PybulletCellModel, compliance_cost, uniform_precision, DirectCollocationOptimizer,ForwardKinematicsOptimizer,cost_functions,DirectKinematicsOptimizer
import pybullet_industrial as pi
import casadi as ca


def optimize_joint_states(urdf):

    cell_urdf = urdf
 
    robot_cell = PybulletCellModel(cell_urdf, 'end_effector', gui=False, workstation_frames = ["workstation"], circle_radius=0.1)

    toolpath = pi.linear_interpolation(np.array([2.0, 3.0, 1.0]), [1.0, 0.5, 1.0], 2, [1,0,0,0], [1,0,0,0])

    #toolpath.draw(color=[1,0,0])

    optimizer = DirectCollocationOptimizer(robot_cell,
                                           [[toolpath.positions, toolpath.orientations]],
                                           [0.4]*5,
                                           [cost_functions.uniform_precision_minimum_movement],
                                           workstation_names=["workstation"],
                                           redundant_z=False)

   
    solution = optimizer.optimize_2d_paths(initial_design_joints=[1,1,1])
    optimized_values = solution.value(optimizer.q_design)
    # Apply the optimized design state to the robot
    robot_cell.set_design_state(solution.value(optimizer.q_design), 300)
    #joint_states = robot_cell.set_design_state(solution.value(optimizer.q_design), 200)
    print("This is the endeffector pose of robot cell: ",robot_cell.robot.get_endeffector_pose("end_effector"))
    print("These are the joint states of robot cell: ",robot_cell.robot.get_joint_state())
    p.disconnect()
    
    """    print("Optimized Design State:", optimized_values)
    pi.draw_point((0.0, 4.0, 1.0), length=0.05)
    pi.draw_point((2.0, 0.0, 1.0), length=0.05)"""
 
    """# Extract and plot the joint trajectory
    joint_trajectory = solution.value(optimizer.q_moving)
    print("This is the join trajectory i guess: ", joint_trajectory)
    plt.figure()
    plt.plot(joint_trajectory.T)
    plt.title('Joint Trajectory')
    plt.xlabel('Step')
    plt.ylabel('Joint Position')
    plt.show()

     #Continuous simulation loop (this will keep the simulation running)
    while True:
        for i, joint_values in enumerate(joint_trajectory.T):

            if i == 0:
                robot_cell.set_joint_position(joint_values,True)

                robot_cell._execute_simulation_steps(0, 400)
            else:
                robot_cell.set_joint_position(joint_values,True)

                robot_cell._execute_simulation_steps(0.1, 220)"""
            
    
    return (robot_cell,optimized_values)

optimize_joint_states("C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/scaraRobot.urdf")




    
   