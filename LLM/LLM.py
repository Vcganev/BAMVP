import os
import marvin
from openai import OpenAI

client = OpenAI()

def get_robot_recommendation(task_description):

    model = 'gpt-4'
    system_message = {
        "role": "system",
        "content": "As a mechanical engineer working in the industry, your responsibility involves pinpointing and selecting the ideal robotic type for a specified task. Only give out the Robot type, no explanation or anything else. Just the Solution!"
    }

    user_message = {
        "role": "user",
        "content": task_description
    }

    num_iterations = 20
    responses = []

    for _ in range(num_iterations):
        completion = client.chat.completions.create(
            model=model,
            messages=[system_message, user_message],
            temperature = 0.8
        )
        responses.append(completion.choices[0].message.content)

    print("ChatGPT Output: ", responses)

    robot_type = marvin.classify(

        responses,
        labels=["Scara Robot", "Articulated Robot", "Gantry Robot", "Delta Robot"]

    )

    print("Marvin Output: ", robot_type)
    
    return robot_type

def evaluate_choice(robot_type, task_description, simulation_result):
    model = 'gpt-4'
    system_message = {
        "role": "system",
        "content": "As a mechanical engineer working in the industry, your responsibility involves pinpointing and selecting the ideal robotic type for a specified task. Previously you selected a robot type based on a specific task description. After simulating this, your job now is to evaluate whether it was a good choice or not."
    }

    user_message = {
        "role": "user",
        "content": f"You previously picked a robot type based on a use case. This robot was simulated to see if it can reach the needed points. Your job now is to look at the simulation data and choose whether it was the right choice or not. The variable 'success' already states whether the simulation was successful or not, but I want you to look at the points that were reached and whether it matches the trajectory and then evaluate whether this robot was the right choice or not. If it was not the right choice I wan't you to give an explanation, why it wasn't and also what would need to be focused on when choosing again. Simulation Results: Choosen Roboter: {robot_type} Use Case: {task_description} Simulation Results: {simulation_result}"
    }

    completion = client.chat.completions.create(
            model=model,
            messages=[system_message, user_message],
            temperature = 0.8
        )
    
    llm_evaluation = completion.choices[0].message.content
    print("ChatGPT Output: ", llm_evaluation)

    choice_success = marvin.classify(
        llm_evaluation,
        labels=["Yes", "No"]

    )
    if choice_success == "Yes":
        return "THE CHOICE AND SIMULATION WAS A SUCCESS"
    else:
        return "THATS THE WRONG BOT!"
