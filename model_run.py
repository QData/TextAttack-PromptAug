import chatgpteval
import flant5eval
import maze_descriptor
import importlib
import sys

"""
    Args: 
        model_name: the name selected from the model_names.
        form_number: which form to choose.
        report_folder: the folder name to store the report result.
    gen_new_maze:

"""
def run_model(model_name, form_number, report_folder):

    model_select = model_name + "eval"
    mod = importlib.import_module(model_select)
    mod.report_gen(form_number, report_folder)

if __name__ == '__main__':
    model_names = ["chatgpt", "flant5"]
    model_name = input('Select from model: chatgpt, flant5: ')
    prompt_index = input('Select from the prompt 1, 2: ')
    report_folder = input('Type the folder name you want to save the report: ')
    index = -1
    for i in range(len(model_names)):
        if model_name == model_names[i]:
            index = i
    if index == -1:
        print("Model not found")
        sys.exit()
    


    run_model(model_names[index], prompt_index, report_folder)

    

    
    

    
    