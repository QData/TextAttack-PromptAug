import torch
import random
import json
import os

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration
from question_generator import QuestionGenerator


if __name__ == "__main__":
    CACHE_DIR = "/p/qdatatext/ki4km/models/"
    DATA_DIR = "datasets/data/canvases"

    is_gpu = torch.cuda.is_available()

    if is_gpu:
        print("Using GPU")
    else:
        print("Using CPU")

    # tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B", cache_dir=CACHE_DIR)
    # model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", device_map="auto", cache_dir=CACHE_DIR)
    # subfolder = "GPT-J"

    # tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl", cache_dir=CACHE_DIR)
    # model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto", cache_dir=CACHE_DIR)
    subfolder = "T5"

    results_folder = f"results/{subfolder}/transitivity"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    positive = 0
    negative = 0
    n_examples = 100
    for i in range(0, n_examples):
        filepath = f"{DATA_DIR}/canvas_3_{i}.json"
        outpath = f"{results_folder}/canvas_3_{i}.json"

        gen = QuestionGenerator.from_file(filepath)
        #questions = gen.generate_existence_questions()

        # Have an even split
        # is_answer_yes = i < (n_examples // 2) 
        # if is_answer_yes:
        #     question = random.choice([question for question, answer in questions if answer == "Yes"])
        #     expected = "Yes"
        # else:
        #     question = random.choice([question for question, answer in questions if answer == "No"])
        #     expected = "No"

        # input_string = gen.generate_full_description() + question + " Answer with 'Yes' or 'No'.\nAnswer:"
        # question = "Is there a yellow shape in the canvas?"
        #input_string = gen.generate_full_description() + "\nIs there a yellow triangle in the canvas?" + "\nAnswer: No\n" + question + "\nAnswer:"
        #input_string = gen.generate_full_description() + f"\nQuestion: {question}" + "\nAnswer:"

        # input_string = gen.generate_short_description() + f"\nQuestion: {question}" + "\nAnswer:"
        #input_string = gen.generate_short_description() + question + "\nAnswer:"

        input_string, expected = gen.generate_transitivity_promopt(horizontal=True)
        question = input_string.split("Question")[1]

        print(input_string)
        exit()

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

        # if is_answer_yes and "yes" in answer.lower():
        #     positive += 1
        # elif not is_answer_yes and "no" in answer.lower():
        #     negative += 1

        with open(outpath, "w") as f:
            result = {
                "context": input_string, 
                "question": question, 
                "expected": expected,
                "actual": answer
            }
            json.dump(result, f, indent=4)  

    # Print results
    # print(f"Accuracy: {(positive + negative) / n_examples}")
    # print(f"Positive Accuracy: {positive / (n_examples // 2)}")
    # print(f"Negative Accuracy: {negative / (n_examples // 2)}")
