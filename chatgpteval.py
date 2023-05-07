"""
This file is used to evaluate the performance of chatGPT.
"""


import openai
from point_calculate import point_calculation
import promptform
import json
import os

# openai key
openai.api_key = ''
# The folder that stores the mazes infomation.
maze_folder = "maze_json"

def report_gen(form_number, report_folder):

    #Initialize the maximum point that the test can get and the point it actually gets for four aspects. 
    full = 0
    get = [0,0,0,0]

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    #Iterate over the files in the maze folder
    for file_name in os.listdir(maze_folder):
            with open(os.path.join(maze_folder, file_name)) as f:
                print("file running:" + file_name)
                full += 1

                # Generate the prompt
                data = json.load(f)
                prompt_func = getattr(promptform, "prompt" + str(form_number)) 
                s = prompt_func(data["start position"], data["end position"], data["canvas size"], data["obstacles"])
                
                # Run the model, receive the reply
                messages = []
                if s:
                    messages.append(
                    {"role": "user", "content": s},
                    )
                chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens= 400)
                reply = chat.choices[0].message.content
                print(f"ChatGPT: {reply}")

                # Calculate the points
                p = point_calculation(data["start position"], data["end position"], reply, data["obstacles"])
                one_p = p.point_calculate()
                get[0] += one_p[0]
                get[1] += one_p[1]
                get[2] += one_p[2]
                get[3] += one_p[3]

                # Write the report for each individual maze to the destination folder
                with open(report_folder + "/" + file_name + "prompt.txt", "w") as f:
                    f.write(s)
                    f.write("\n\n")
                    f.write(reply)
                    f.write("\n\n")
                    f.write(f"point get {one_p}")

    # Write the summary for the test into the destination folder            
    with open(report_folder + "/" + "summary", "w") as f:
        f.write(f"Correct start end place: {get[0]}\nOne step every move: {get[1]} \ndirection and coordinate match: {get[2]} \nBarrier detecting: {get[3]}")

    # print(full)
    # print(get)