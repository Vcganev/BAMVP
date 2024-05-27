import pybullet as p
import shutil
import time
import numpy as np
import xml.etree.ElementTree as ET
from robot_setups import setups
from simulation import environment
from LLM import LLM
import optimizer
import pybullet_industrial as pi


new_joint_values = {
    "design_prismatic1_z": 0.85,       # new value for joint design_prismatic1_z
    'design_prismatic2_x': 2.7529257,  # new value for joint design_prismatic2_x
    "design_prismatic3_x": 0.50227065  # new value for joint design_prismatic3_x
}

def main():

    urdf_file = "C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/scaraRobot.urdf"
    urdf_file_2 = "C:/Users/victo/Downloads/test2.urdf"
    
    start_orientation = p.getQuaternionFromEuler ([0, 0, 0])
    # robot = pi.RobotBase(urdf_file, [0, 0, 0], start_orientation, 'end_effector')
    robot_cell, joint_values = optimizer.optimize_joint_states(urdf_file)
    print("These are the joint values inside of the test", joint_values)
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(numSolverIterations=1500)
    time.sleep(5)
    
    toolpath = pi.linear_interpolation(np.array([1.0, 4.0, 1.0]), [2.0, 0.0, 1.0], 2, [1,0,0,0], [1,0,0,0])
    toolpath.draw(color=[1,0,0])
    
    robot = pi.RobotBase(urdf_file_2, [0, 0, 0], start_orientation, 'end_effector')
    
    # Funktion um die Werte der Prismatischen Gelenke von urdf1 auf fixed gelenke in urdf 2 zu übertragen
    modify_urdf_with_optimized_lengths_2(urdf_file, urdf_file_2, joint_values)
    
    # 4 Debugging
    print("current joint state", robot.get_joint_state())
    
  
    """    robot.set_joint_position(new_joint_values, ignore_limits = True)
    num_steps = 200
    for _ in range (num_steps):
        p.stepSimulation()
    print("These are the joint states after setting them:", robot.get_joint_state())"""

    trajectory = [((2.0, 3.0, 1.0), (1.0, 0.0, 0.0, 0.0)), ((1.0, 0.5, 1.0), (1.0, 0.0, 0.0, 0.0))]
        # more tuples/lists following the same structure

    """positions = np.array(toolpath.positions)
    orientations = np.array(toolpath.orientations)
    trajectory_2 = []
    for i in range(positions.shape[1]):  # Assuming the number of positions and orientations match
        position_tuple = tuple(positions[:, i])
        orientation_tuple = tuple(orientations[:, i])
        trajectory_2.append((position_tuple, orientation_tuple))


    trajectory_3 = [[toolpath.positions, toolpath.orientations]]
    """
    print("This is the trajectory 1: ", trajectory)
    #print("This is the trajectory 2:", trajectory_2)

    pi.draw_point((1.0, 4.0, 1.0), length=0.05)
    pi.draw_point((2.0, 0.0, 1.0), length=0.05)

    simulationEnvironment = environment.MetaPybulletIndustrialEnvironment(robot, trajectory)
    positions, orientations = simulationEnvironment.run_simulation()
    print("These are the joint states after the simulation: ", robot.get_joint_state())
    evaluate_results = simulationEnvironment.evaluate(positions, orientations)
    print(evaluate_results)
    

def modify_urdf_with_optimized_lengths_1(urdf_path, optimized_lengths):
    """
    Modifies the lengths of links in a URDF file according to optimized results.
    
    Args:
    - urdf_path (str): Path to the URDF file to modify.
    - optimized_lengths (list): List of optimized lengths corresponding to the links in the URDF.
    """
    tree = ET.parse(urdf_path)
    root = tree.getroot()

    # Update the length of the first arm link
    link1 = root.find(".//link[@name='link1']/visual/geometry/cylinder")
    if link1 is not None:
        link1.set('length', str(optimized_lengths[1]))  # Optimized length for the first arm link

    # Update the origin of the first joint, if necessary (if there was a prismatic joint modifying the base height)
    joint1_origin = root.find(".//joint[@name='joint1']/origin")
    if joint1_origin is not None:
        joint1_origin.set('xyz', f"0 0 {optimized_lengths[0]}")  # Assuming the first value affects base height

    # Update the length of the second arm link
    link2 = root.find(".//link[@name='link2']/visual/geometry/cylinder")
    if link2 is not None:
        link2.set('length', str(optimized_lengths[2]))  # Optimized length for the second arm link

    # Save the modified URDF
    tree.write(urdf_path)
    print(f"URDF file '{urdf_path}' updated with optimized lengths.")
    

def modify_urdf_with_optimized_lengths_2(input_urdf_path, output_urdf_path, optimized_values):
    
    """
    Copies the original URDF to a new file and modifies it to set prismatic joints to fixed values based on optimization results.

    Args:
    - input_urdf_path (str): Path to the original URDF file.
    - output_urdf_path (str): Path where the modified URDF will be saved.
    - optimized_values (list): List of optimized lengths for the prismatic joints.
    """
    # Copy the original URDF to a new file
    shutil.copy(input_urdf_path, output_urdf_path)

    # Load the copied URDF file to modify
    tree = ET.parse(output_urdf_path)
    root = tree.getroot()

    # Update the first prismatic joint to a fixed joint
    joint1 = root.find(".//joint[@name='design_prismatic1_z']")
    if joint1 is not None:
        joint1.set('type', 'fixed')
        joint1.find('.//origin').set('xyz', f"0 0 {optimized_values[0]}")

    # Update the second prismatic joint to a fixed joint
    joint2 = root.find(".//joint[@name='design_prismatic2_x']")
    if joint2 is not None:
        joint2.set('type', 'fixed')
        joint2.find('.//origin').set('xyz', f"{optimized_values[1]} 0 0")

    # Update the third prismatic joint to a fixed joint
    joint3 = root.find(".//joint[@name='design_prismatic3_x']")
    if joint3 is not None:
        joint3.set('type', 'fixed')
        joint3.find('.//origin').set('xyz', f"{optimized_values[2]} 0 0")

    # Save the modified URDF
    tree.write(output_urdf_path)
    print(f"Modified URDF saved to {output_urdf_path}")



if __name__ == "__main__":
    main()
    
    
    