import argparse
import torch
import random
import json
import os

from datasets.loader import ShapeDataset
from datasets.constants import DESCRIPTION_TYPES, MODEL_NAMES
from datasets.tasks.registered_tasks import tasks
from models.model import Model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", choices=MODEL_NAMES, required=True, 
        help="The name of the model to run")
    parser.add_argument("-d", "--description", choices=DESCRIPTION_TYPES, required=True,
        help="The name of the description type to provide to the model")
    parser.add_argument("-q", "--question", choices=[task.name for task in tasks], required=True,
        help="The name of the task to run the model on")
    parser.add_argument("-s", "--num-shapes", default=1, type=int, 
        help="The number of shapes in the canvas")
    parser.add_argument("-n", "--num-examples", default=0, type=int, 
        help="The number of canvases to run")
    parser.add_argument("-f", "--few-shot", action="store_true", 
        help="Inputs are few-shot if set")
    args = parser.parse_args()

    is_gpu = torch.cuda.is_available()
    if is_gpu:
        print("Using GPU...\n")
    else:
        print("Using CPU...\n")


    data = ShapeDataset(args.num_shapes, args.description, args.question, args.few_shot)
    model = Model(args.model, is_gpu)
    subfolder = args.model.upper()

    results_folder = f"results/{subfolder}/{args.question}/{'few_shot' if args.few_shot else ''}"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    correct = 0
    for i in range(0, args.num_examples):

        outpath = f"{results_folder}/canvas_{args.num_shapes}_{i}.json"
        description, question, expected = data[i]
        input_string = description + "\nQuestion: " + question

        answer = model.generate(input_string)

        with open(outpath, "w") as file:
            result = {
                "description": description,
                "question": question, 
                "expected": expected,
                "actual": answer
            }
            json.dump(result, file, indent=4)  

