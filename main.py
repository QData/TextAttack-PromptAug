import argparse
import torch
import random
import json
import os

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration

from datasets.loader import ShapeDataset


if __name__ == "__main__":
    CACHE_DIR = "/p/qdatatext/ki4km/models/"

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", choices=["gpt-j", "flan-t5", "flan-ul2"], required=True)
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

    if args.model == "flan-ul2":
        tokenizer = T5Tokenizer.from_pretrained("google/flan-ul2", cache_dir=CACHE_DIR)
        model = T5ForConditionalGeneration.from_pretrained("google/flan-ul2", device_map="auto", cache_dir=CACHE_DIR, torch_dtype=torch.bfloat16)
        subfolder = "FLAN-UL2"
    elif args.model == "flan-t5":
        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl", cache_dir=CACHE_DIR)
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto", cache_dir=CACHE_DIR)
        subfolder = "FLAN-T5"
    elif args.model == "gpt-j":
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B", cache_dir=CACHE_DIR)
        model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", device_map="auto", cache_dir=CACHE_DIR)
        subfolder = "GPT-J"


    results_folder = f"results/{subfolder}/{args.question}"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    correct = 0
    data = ShapeDataset(args.num_shapes, args.description, args.question)
    for i in range(0, args.num_examples):
        outpath = f"{results_folder}/canvas_{args.num_shapes}_{i}.json"
        description, question, expected = data[i]
        input_string = description + "\nQuestion: " + question

        input_ids = tokenizer(input_string, return_tensors="pt").input_ids
        if is_gpu:
            input_ids = input_ids.to("cuda")

        outputs = model.generate(
            input_ids, 
            max_new_tokens=10,
            top_p=0.9,
            do_sample=False,
            early_stopping=False,
        )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if args.model == "gpt-j":
            answer = answer[len(input_string):]

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

