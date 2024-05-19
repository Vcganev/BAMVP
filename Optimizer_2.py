import os
import numpy as np
import matplotlib.pyplot as plt
from rolap import PybulletCellModel, compliance_cost, uniform_precision, DirectCollocationOptimizer
import pybullet_industrial as pi
import casadi as ca

if __name__ == "__main__":
    # Define the path to your robot's URDF file
    cell_urdf = "C:/Users/victo/OneDrive/Dokumente/BA/Matlab/reachabilityExperiment/Ex_1_scaraRobot4/scaraRobot4 - Kopie.urdf"  # Update this path to your URDF file location

    # Initialize the robot cell model with no workstations
    robot_cell = PybulletCellModel(cell_urdf, 'end_effector', workstation_frames=[], circle_radius=0.1)

    # Generate a simple toolpath (example path, adjust as necessary)
    toolpath = pi.build_box_path(np.array([0, 0, 0.2]), [0.5, 0.6], 0.1, [0, 0, 0, 1], 80)

    # Optionally draw the toolpath for visualization
    toolpath.draw(color=[1, 0, 0])

    # Prepare the optimizer using the toolpath, assuming you're using two similar toolpaths for demonstration
    optimizer = DirectCollocationOptimizer(robot_cell,
                                           [[toolpath.positions, toolpath.orientations], [toolpath.positions, toolpath.orientations]],
                                           [10**-6]*6 + [0]*8,
                                           [compliance_cost, compliance_cost],
                                           [],  # Empty list for workstations
                                           points_per_transition=10, redundant_z=False)

    # Optimize the 2D paths
    solution = optimizer.optimize_2d_paths(initial_design_joints=[2, 0, 0, 0, 1.5, 2, 0, 0])

    # Apply the optimized design state to the robot
    robot_cell.set_design_state(solution.value(optimizer.q_design), 200)

    # Extract and plot the joint trajectory
    joint_trajectory = solution.value(optimizer.q_moving)
    plt.figure()
    plt.plot(joint_trajectory.T)
    plt.title('Joint Trajectory')
    plt.xlabel('Step')
    plt.ylabel('Joint Position')
    plt.show()

    # Continuous simulation loop (this will keep the simulation running)
    while True:
        for i, joint_values in enumerate(joint_trajectory.T):
            if i == 0:
                robot_cell.set_joint_position(joint_values, ignore_limits=True)
                robot_cell._execute_simulation_steps(0, 400)
            else:
                robot_cell.set_joint_position(joint_values, ignore_limits=True)
                robot_cell._execute_simulation_steps(0.0000001, 60)
