import argparse
import torch
import random
import json
import os

from datasets.loader import ShapeDataset
from models.model import Model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", choices=["chat-gpt", "gpt-j", "flan-t5", "flan-ul2"], required=True)
    parser.add_argument("-d", "--description", choices=["full", "partial", "short", "transitive"], required=True)
    parser.add_argument("-q", "--question", choices=["existence", "transitivity"], required=True)
    parser.add_argument("-s", "--num-shapes", default=1, type=int)
    parser.add_argument("-n", "--num-examples", default=0, type=int)
    args = parser.parse_args()

    is_gpu = torch.cuda.is_available()
    if is_gpu:
        print("Using GPU...\n")
    else:
        print("Using CPU...\n")


    model = Model(args.model, is_gpu)
    subfolder = args.model.upper()

    results_folder = f"results/{subfolder}/{args.question}"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    correct = 0
    data = ShapeDataset(args.num_shapes, args.description, args.question)
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

        if expected.lower() in answer.lower():
            correct += 1

    print(f"Accuracy: {correct / args.num_examples:0.4f}")

