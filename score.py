import argparse
import json
import os

from datasets.constants import DESCRIPTION_TYPES, MODEL_NAMES
from datasets.tasks.registered_tasks import tasks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", choices=MODEL_NAMES, required=True)
    parser.add_argument("-q", "--question", choices=[task.name for task in tasks], required=True)
    parser.add_argument("-s", "--num-shapes", type=int, required=True)
    parser.add_argument("-f", "--few-shot", action="store_true")
    args = parser.parse_args()

    subfolder = args.model.upper()
    results_folder = f"results/{subfolder}/{args.question}/{'few_shot' if args.few_shot else ''}"
    if not os.path.isdir(results_folder):
        print("Found no results. Exiting...")
        exit()

    task = [task for task in tasks if task.name == args.question][0]

    total_score = 0
    total = 0
    while True:
        filepath = f"{results_folder}/canvas_{args.num_shapes}_{total}.json"
        if not os.path.isfile(filepath):
            break

        total_score += task.score(filepath)
        total += 1

    print(f"Total Results: {total}")
    print(f"Avereage Score: {total_score / total:0.4f}")

