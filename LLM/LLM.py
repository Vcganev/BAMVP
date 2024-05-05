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
