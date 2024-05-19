import pybullet as p
from robot_setups import setups
from simulation import environment
from LLM import LLM

def get_user_input():
    print("Welcome to the Robot Customization Program!")
    print("Please describe your use case in detail:")
    task_description = input("Use Case: ")

    print("\nGreat! Now, please provide the points and orientations the robot needs to reach.")
    print("Each point should be in the format: (x, y, z)")
    print("Each orientation should be in the format: (qx, qy, qz, qw)")
    print("Example: ((0.0, 3.0, 1.0), (0.0, 0.0, 0.965925, 0.25881905))")

    trajectory = []
    while True:
        point = input("Enter point (or 'done' to finish): ")
        if point.lower() == 'done':
            break
        orientation = input("Enter orientation: ")
        try:
            point_tuple = tuple(map(float, point.strip("()").split(",")))
            orientation_tuple = tuple(map(float, orientation.strip("()").split(",")))
            trajectory.append((point_tuple, orientation_tuple))
        except ValueError:
            print("Invalid input. Please enter the point and orientation in the correct format.")
    
    print("\nYou have entered the following trajectory:")
    for p, o in trajectory:
        print(f"Point: {p}, Orientation: {o}")
    
    confirmation = input("Is this correct? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Let's try again.")
        return get_user_input()
    
    return task_description, trajectory

def main():
    task_description, trajectory = get_user_input()
    robot_type = LLM.get_robot_recommendation(task_description)
    print("Recommended Robot Type: ", robot_type)

    #Hier wird der Optimisierer von Jan aufgerufen
    #Ein neues Robot Objekt mit dem neuen urdf code wird initialisiert
    # Dann wird mit diesem neuen Object die Demo durchgelaufen

    robot_setup = setups.setup_robot_by_type(robot_type)

    #trajectory = [

    #    ((0.0, 3.0, 1.0), (0.0, 0.0, 0.965925, 0.25881905)),
    #    ((3.0, 0.0, 1.0), (0.0, 0.0, 0.5, 0.866)),
        # more tuples/lists following the same structure 
    #]


    simulationEnvironment = environment.MetaPybulletIndustrialEnvironment(robot_setup, trajectory)
    positions, orientations = simulationEnvironment.run_simulation()
    #print("These are the point: ", positions, orientations)
    evaluate_results = simulationEnvironment.evaluate(positions, orientations)
    llm_evaluation = LLM.evaluate_choice(robot_setup, task_description, evaluate_results)
    
    print(llm_evaluation)

    #print("Results: ", evaluate_results)


if __name__ == "__main__":
    main()
