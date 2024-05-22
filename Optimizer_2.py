import os
import numpy as np
import matplotlib.pyplot as plt
from rolap import PybulletCellModel, compliance_cost, uniform_precision, DirectCollocationOptimizer,ForwardKinematicsOptimizer,cost_functions
import pybullet_industrial as pi
import casadi as ca

if __name__ == "__main__":

    cell_urdf = "C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/scaraRobot.urdf" 
 
    robot_cell = PybulletCellModel(cell_urdf, 'end_effector', workstation_frames = ["workstation"], circle_radius=0.1)

    toolpath = pi.linear_interpolation(np.array([0.0, 3.0, 1.0]), [3.0, 0.0, 1.0], 10, [0.0, 0.0, 0.965925, 0.25881905], [0.0, 0.0, 0.5, 0.866])

    toolpath.draw(color=[1,0,0])

    optimizer = DirectCollocationOptimizer(robot_cell,
                                           [[toolpath.positions, toolpath.orientations]],
                                           [10**-6]*6+[0]*8,
                                           [cost_functions.uniform_precision_minimum_movement],
                                           workstation_names=["workstation"],
                                           redundant_z=False)

   
    solution = optimizer.optimize_2d_paths()

    # Apply the optimized design state to the robot
    robot_cell.set_design_state(solution.value(optimizer.q_design), 200)
    
    
    print("This is the Robot Cell", robot_cell)

    # Extract and plot the joint trajectory
    joint_trajectory = solution.value(optimizer.q_moving)
    print("This is the join trajectory i guess: ", joint_trajectory)
    plt.figure()
    plt.plot(joint_trajectory.T)
    plt.title('Joint Trajectory')
    plt.xlabel('Step')
    plt.ylabel('Joint Position')
    plt.show()

    # Continuous simulation loop (this will keep the simulation running)
    #while True:
     #   for i, joint_values in enumerate(joint_trajectory.T):

      #      if i == 0:
       #         robot_cell.set_joint_position(joint_values,True)

        #        robot_cell._execute_simulation_steps(0, 400)
         #   else:
          #      robot_cell.set_joint_position(joint_values,True)

           #     robot_cell._execute_simulation_steps(0.0000001, 60)
