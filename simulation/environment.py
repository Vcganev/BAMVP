import pybullet as p
import pybullet_industrial as pi
import numpy as np
from robot_setups import setups

class MetaPybulletIndustrialEnvironment:
    def __init__(self, setup_function, trajectory_object):
        p.connect(p.DIRECT)
        self.robot = setup_function()
        self.trajectory = trajectory_object
        #print("trajectory object:", trajectory_object)

    # Methode zum Durchführen der Simulation
    def run_simulation(self):
        positions = []
        orientations = []
        for position, orientation in self.trajectory:
            for _ in range(300):
                self.robot.set_endeffector_pose(position, orientation)
                p.stepSimulation()
                #endeffector_pose = self.robot.get_endeffector_pose('end_effector')
                current_position, _ = self.robot.get_endeffector_pose('end_effector')
                _ , current_orientation = self.robot.get_endeffector_pose('end_effector')
            positions.append(current_position)
            orientations.append(current_orientation)
            #print("positions n orientations: ",positions, orientations)
        return positions, orientations
    
    # Methode um die Ergebnisse der Simulation zu evaluieren
    def evaluate(self, positions, orientations):
        reached_points = []
        unreached_points = []
        
        if len(positions) != len(self.trajectory) or len(orientations) != len(self.trajectory):
            return {"success": False, "error": "Mismatch in number of trajectory points and recorded points"}

        for index, ((recorded_pos, recorded_ori), (trajectory_pos, trajectory_ori)) in enumerate(zip(zip(positions, orientations), self.trajectory)):
            if self.is_same_position(recorded_pos, trajectory_pos, 0.05) and self.is_same_orientation(recorded_ori, trajectory_ori, 0.05):
                reached_points.append((index, recorded_pos, recorded_ori))
            else:
                unreached_points.append((index, recorded_pos, recorded_ori))
        
        success = len(unreached_points) == 0
        return {
            "success": success,
            "reached_points": reached_points,
            "unreached_points": unreached_points,
            "positions": positions,
            "orientations": orientations
        }

    def is_same_position(self, p1, p2, tolerance=0.5):
        p1 = np.array(p1)
        p2 = np.array(p2)
        # Check if two positions are the same within a certain tolerance
        return np.all(np.abs(p1 - p2) < tolerance)
    def is_same_orientation(self, o1, o2, tolerance=0.5):
        # Convert inputs to NumPy arrays to ensure correct handling
        o1 = np.array(o1)
        o2 = np.array(o2)
        # Check if two orientations are the same within a certain tolerance
        return np.all(np.abs(o1 - o2) < tolerance)

     




