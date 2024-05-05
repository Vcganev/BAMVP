import pybullet as p
from robot_setups import setups
from simulation import environment
from LLM import LLM

def get_user_input():
    print("Please describe your use case")
    task_description = input ("Description: ")
    return task_description

def main():
    task_description = get_user_input()
    robot_type = LLM.get_robot_recommendation(task_description)
    print("Recommended Robot Type: ", robot_type)

    robot_setup = setups.setup_robot_by_type(robot_type)

    trajectory = [

        ((0.0, 3.0, 1.0), (0.0, 0.0, 0.965925, 0.25881905)),
        ((3.0, 0.0, 1.0), (0.0, 0.0, 0.5, 0.866)),
        # more tuples/lists following the same structure 
    ]


    simulationEnvironment = environment.MetaPybulletIndustrialEnvironment(robot_setup, trajectory)
    positions, orientations = simulationEnvironment.run_simulation()
    #print("These are the point: ", positions, orientations)
    evaluate_results = simulationEnvironment.evaluate(positions, orientations)

    print("Results ", evaluate_results)


if __name__ == "__main__":
    main()
