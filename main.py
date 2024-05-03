import pybullet as p
from robot_setups import setups
from simulation import environment

trajectory = [

    ((0.0, 3.0, 1.0), (0.0, 0.0, 0.0, 1)),
    ((3.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1)),
    # more tuples/lists following the same structure
]


simulationEnvironment = environment.MetaPybulletIndustrialEnvironment(setups.setup_scaraRobot, trajectory)
positions, orientations = simulationEnvironment.run_simulation()
#print("These are the point: ", positions, orientations)
evaluate_results = simulationEnvironment.evaluate(positions, orientations)

print("Results ", evaluate_results)