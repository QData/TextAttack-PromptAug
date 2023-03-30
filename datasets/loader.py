import json
import os
import random

from torch.utils.data import Dataset


class ShapeDataset(Dataset):
    def __init__(self, n_shapes, description_type, question_type, data_dir="data"):

        valid_description_types = {"full", "partial", "short", "transitive"}
        if description_type not in valid_description_types:
            raise ValueError(f"Description type must be one of {valid_description_types}")

        valid_question_types = {"existence", "transitivity"}
        if question_type not in valid_question_types:
            raise ValueError(f"Question type must be one of {valid_question_types}")

        if n_shapes < 2 and question_type == "transitivity":
            raise ValueError("Transitive questions are only valid for 3 or more shapes")

        self.description_type = description_type
        self.question_type = question_type

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


    def __len__(self):
        return len(self.data_files)


    def __getitem__(self, idx):
        with open(f"{self.data_dir}/{self.data_files[idx]}", "r") as file:
            data = json.load(file)

        description = data["descriptions"][self.description_type]
        question, answer = data["questions"][self.question_type]
        return description, question, answer

