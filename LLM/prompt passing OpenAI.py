import os
import marvin
from openai import OpenAI

client = OpenAI()

urdf_codes = {
    "Scara 1": "path/to/scara1.urdf",
    "Scara 2": "path/to/scara2.urdf",
    "Scara 3": "path/to/scara3.urdf",
    "Gantry 1": "path/to/gantry1.urdf",
    "Gantry 2": "path/to/gantry2.urdf",
    "Gantry 3": "path/to/gantry3.urdf",
    "Articulated 1": "path/to/articulated1.urdf",
    "Articulated 2": "path/to/articulated2.urdf",
    "Articulated 3": "path/to/articulated3.urdf"
}


model = 'gpt-4'
system_message = {
        "role": "system",
        "content": """
        As a mechanical engineer working in the industry, your responsibility involves pinpointing and selecting the ideal robotic type for a specified task.
        You get to choose from a list of differnet Robots and configurations that are available. Only choose from that List! Never make up a Robot!
        Robot Options:

        SCARA Robots:
        SCARA 1:
            - DoF: 3 (2 revolute, 1 prismatic)
            - Reach: 5m (2m per arm link + 1m prismatic extension)
            - Speed Limits: 0.7 rad/s (revolute), 0.3 m/s (prismatic)
            - Joints Effort: 1200 (revolute), 600 (prismatic)
        SCARA 2:
            - DoF: 4 (3 revolute, 1 prismatic)
            - Reach: 4m (1.5m per arm link + 1m prismatic extension)
            - Speed Limits: 0.6 rad/s (revolute), 0.25 m/s (prismatic)
            - Joints Effort: 800 (revolute), 400 (prismatic)
        SCARA 3:
            - DoF: 3 (2 revolute, 1 prismatic)
            - Reach: 6m (2.5m per arm link + 1m prismatic extension)
            - Speed Limits: 0.8 rad/s (revolute), 0.4 m/s (prismatic)
            - Joints Effort: 1000 (revolute), 700 (prismatic)

        Gantry Robots:
        Gantry 1:
            - DoF: 3 (all linear)
            - Reach: 3m x 3m x 3m (XYZ)
            - Speed Limits: 0.5 m/s (all axes)
            - Joints Effort: 500 (all axes)
        Gantry 2:
            - DoF: 4 (3 linear, 1 rotational)
            - Reach: 4m x 4m x 2m (XYZ)
            - Speed Limits: 0.4 m/s (linear), 0.3 rad/s (rotational)
            - Joints Effort: 600 (linear), 300 (rotational)
        Gantry 3:
            - DoF: 3 (all linear)
            - Reach: 2m x 2m x 4m (XYZ)
            - Speed Limits: 0.6 m/s (all axes)
            - Joints Effort: 700 (all axes)

        Articulated Robots:
        Articulated 1:
            - DoF: 6
            - Reach: 2.5m
            - Speed Limits: 0.5 rad/s (all joints)
            - Joints Effort: 850 (all joints)
        Articulated 2:
            - DoF: 7
            - Reach: 3m
            - Speed Limits: 0.4 rad/s (all joints)
            - Joints Effort: 1000 (all joints)
        Articulated 3:
            - DoF: 5
            - Reach: 1.8m
            - Speed Limits: 0.6 rad/s (all joints)
            - Joints Effort: 900 (all joints)
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
