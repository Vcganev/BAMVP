import os
import marvin
from openai import OpenAI

client = OpenAI()

urdf_codes = {
    "Scara Robot": "C:/Users/victo/OneDrive/Dokumente/BA/REALMVP/BAMVP/URDF Codes/scaraRobot.urdf",
    "Gantry Robot": "path/to/gantry3.urdf",
    "Articulated Robot": "path/to/articulated1.urdf",
}


model = 'gpt-4'
system_message = {
        "role": "system",
        "content": """
        As a mechanical engineer working in the industry, your responsibility involves pinpointing and selecting the ideal robotic type for a specified task.
        You get to choose from a list of differnet Robots and configurations that are available. Only choose from that List! Never make up a Robot!
        Robot Options:

        SCARA Robot:
            - DoF: 3 (2 revolute, 1 prismatic)
            - Reach: between 0m and 10m 

        Gantry Robots:
        Gantry 1:
            - DoF: 3 (all linear)
            - Reach: up to 10m x 10m x 10m (XYZ)

        Articulated Robots:
        Articulated 1:
            - DoF: 6
            - Reach: up to 5m
        """
}

user_message = {
        "role": "user",
        "content": "A robot is needed for the precise placement of delicate electronic components within a confined assembly area, requiring high precision (±0.02 mm), a reach of up to 2 meters, a payload capacity of up to 2 kg, and compact size for small workspaces."
}



completion = client.chat.completions.create(
model=model,
messages=[system_message, user_message],
temperature = 0.8
)

response = (completion.choices[0].message.content)

print("ChatGPT Output: ", response)


robot_type = marvin.classify(

    response,
    labels=["Scara 1", "Scara 2", "Scara 3", "Gantry 1", "Gantry 2", "Gantry 3", "Articulated 1", "Articulated 2", "Articulated 3" ]

)

print("Marvin Output: ", robot_type)

selected_robot_urdf = urdf_codes[robot_type]
print("URDF Code for Selected Robot: ", selected_robot_urdf)
    

# if else statement oder andere art und weise von storage (tabelle?), wo gewählt wird welcher urdf code zu welchem roboter typ gehört
