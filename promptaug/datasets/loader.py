import json
import os
import random

from torch.utils.data import Dataset
from datasets.constants import DESCRIPTION_TYPES
from datasets.tasks.registered_tasks import tasks


class ShapeDataset(Dataset):
    def __init__(self, n_shapes, description_type, question_type, is_few_shot, data_dir="data"):

        if description_type not in DESCRIPTION_TYPES:
            raise ValueError(f"Description type must be one of {valid_description_types}")

        if question_type not in [task.name for task in tasks]:
            raise ValueError(f"Question type must be one of {valid_question_types}")

        if n_shapes < 2 and question_type == "transitivity":
            raise ValueError("Transitive questions are only valid for 3 or more shapes")

        self.description_type = description_type
        self.question_type = question_type
        self.is_few_shot = is_few_shot

        def is_data_file(filename):
            root, ext = os.path.splitext(filename)
            # Remove directories
            if ext != ".json":
                return False
            # Files should be named as canvas_{n_shapes}_{#}.json
            split = filename.split("_")
            if len(split) != 3:
                return False
            return int(split[1]) == n_shapes

        dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(dir, data_dir)
        self.data_files = [filename for filename in os.listdir(self.data_dir) if is_data_file(filename)]
        self.data_files.sort(key=lambda filename: int(filename.split("_")[2].split(".")[0]))

        if len(self.data_files) == 0:
            raise ValueError(f"There is no generated for {n_shapes} shapes. Please generate data first.")


    def __len__(self):
        return len(self.data_files)


    def __getitem__(self, idx):
        with open(f"{self.data_dir}/{self.data_files[idx]}", "r") as file:
            data = json.load(file)

        description = data["descriptions"][self.description_type]
        qa = data["questions"][self.question_type]

        # The ExistenceTrackingTask adds to the description
        if self.question_type == "existence_tracking":
            description += data["descriptions"]["existence_tracking"]

        # If few-shot, add the example question and answers to the description
        if self.is_few_shot:
            for question, answer in qa[1:]:
                description += f"\nQuestion: {question}\nAnswer: {answer}"

        # The first question-answer pair is always the question to ask
        question, answer = qa[0]
        
        return description, question, answer

