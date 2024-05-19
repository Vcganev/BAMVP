import os
import rolap
import numpy as np
import pybullet_industrial as pi
import matplotlib.pyplot as plt
import casadi as ca

# This is an example setup. You'll need to adapt it based on the actual data structure and methods expected by the library.
def create_dummy_workstation(robot_model):
    # Assuming the robot_model has an attribute for storing workstation data
    robot_model.workstation_collision_objects['dummy'] = [
        [0, 0, 0, 1]  # Dummy sphere data: x, y, z, radius
    ]

    # Overriding methods to return default values
    robot_model.workstation_position = lambda joint_pos, name: np.array([0, 0, 0])
    robot_model.workstation_orientation = lambda joint_pos, name: np.array([1, 0, 0, 0])  # Quaternion for no rotation

def main():
    # Define the path to the URDF file

    cell_urdf = "C:/Users/victo/OneDrive/Dokumente/BA/Matlab/reachabilityExperiment/Ex_1_scaraRobot4/scaraRobot4 - Kopie.urdf"
    
    #Initializing the PybulletCellModel with the Urdf and the endeffector link name
    robot_cell = rolap.PybulletCellModel(cell_urdf, 'end_effector', workstation_frames=[])    
    
    #create a dummy workstation
    create_dummy_workstation(robot_cell)
    
    #trajectory for the robot
    #trajectory = [
    #   (np.array([[0.0, 3.0, 1.0], [3.0, 0.0, 1.0]]),
    #  np.array([[0.0, 0.0, 0.965925, 0.25881905], [0.0, 0.0, 0.5, 0.866]]))
    #]

    toolpath = pi.build_box_path(np.array([0, 0, 0.2]), [0.5, 0.6], 0.1, [0, 0, 0, 1], 80)
   
   
    optimizer = rolap.ForwardKinematicsOptimizer(robot_cell, [[toolpath.positions, toolpath.orientations],[toolpath.positions, toolpath.orientations]],[10**-6]*6+[0]*8,design_cost=rolap.uniform_precision, workstation_names = [],redundant_z=False)

    solution = optimizer.optimize_2d_paths()
    
    robot_cell.set_design_state(solution.value(optimizer.q_design),200)
    
    joint_trajectory = solution.value(optimizer.q_moving)
    
    # plot joint trjectory
    plt.figure()
    plt.plot(joint_trajectory.T)
    plt.show()
    
  

if __name__ == "__main__":
    main()
