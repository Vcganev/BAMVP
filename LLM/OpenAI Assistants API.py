import os
import marvin
from openai import OpenAI
import pybullet as p

client = OpenAI()


#Setting up the Assistant
assistant = client.beta.assistants.create(
    name= "MVP_Assistant",
    description= "OpenAI Assistant for BA",
    instructions="You are a mechanical Engineer. Your Job is to choose the right Robot from your Database, based on the Use Case of the User. Just provide the name of the file of the chosen Robot in your Database.",
    model= "gpt-4-turbo",
    tools=[{"type":"file_search"}],
)


#Creating a Vector Store for the Robot files:
vector_store = client.beta.vector_stores.create(name = "Robot_Files")

file_paths = ["C:/Users/victo/OneDrive/Dokumente/BA/OpenAI Assistant's API/URDF Codes/Gantry Robot.txt", "C:/Users/victo/OneDrive/Dokumente/BA/OpenAI Assistant's API/URDF Codes/Scara Robot 1.txt"]
file_streams = [open(path, "rb") for path in file_paths ]

#Using the upload an poll SDK helper to upload the files, add them to the vector store,
#and poll the status of the file batch for completion

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

#Printing the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)


assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)


thread = client.beta.threads.create(
    messages = [
        {
            "role": "user",
            "content": "I want a Robot that is able to reach these points: A [3, 0, 1] B[0, 3, 1] C [-3, 0, 1] D[0, -3, 1]."
        
        }

    ]

)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread.id))

# Print each message's content and check for annotations
for message in messages:
    print("Message Content:", message.content)
    if hasattr(message, 'annotations'):
        for annotation in message.annotations:
            print("Annotation:", annotation)
    else:
        print("No annotations present.")

message_content = messages[0].content[0].text
annotations = message_content.annotations
citations = []
for index, annotations in enumerate (annotations):
    message_content.value = message_content.value.replace(annotations.text, f"[{index}]")
    if file_citation := getattr(annotations, "file citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}]{cited_file.filename}")


print("testing this shit: ", message_content.value)
#print("/n".join(citations))
print(citations)
