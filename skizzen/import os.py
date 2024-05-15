import os
import marvin
from openai import OpenAI
import pybullet as p

client = OpenAI()

def get_robot_recommendation():

    model = 'gpt-4'
    system_message = {
        "role": "system",
        "content": "You are a developer that writes urdf code"
    }

    user_message = {
        "role": "user",
        "content": "You are a mechanical Engineer. I want you to write an urdf code for a Scara Robot that can reach these Points: A [3, 0, 1] B[0, 3, 1] C [-3, 0, 1] D[0, -3, 1]. Write the full urdf code and don't leave anything up to me. I want to be able to just copy paste the code."
    }


    completion = client.chat.completions.create(
        model=model,
        messages=[system_message, user_message],
        temperature = 0.8
        )
    response = completion.choices[0].message.content

    print("ChatGPT Output: ", response)

    marvin_code = marvin.cast( response, target= str, instructions = "Just the urdf code that is inside of the text")

    print("Marv: ", marvin_code)



def is_urdf_loadable(urdf_string):
    try:
        p.connect (p.DIRECT)
        with open("temp.urdf", "w") as temp_file:
            temp_file.write(urdf_string)
            p.loadURDF("temp.urdf")
            p.disconnect()
            return "This urdf Code is loadable"
    except:
        return "This urdf code is not loadable"
    
urdf_code = get_robot_recommendation()
loadable = is_urdf_loadable(urdf_code)
print(loadable)