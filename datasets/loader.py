import json
import os
import random

from torch.utils.data import Dataset



class ShapeDataset(Dataset):

    def __init__(self, n_shapes, description_dir="data/descriptions", qa_dir="data/questions"):
        # Verify the number of descriptions and qa match
        dir = os.path.dirname(__file__)
        self.description_dir = os.path.join(dir, description_dir)
        self.description_files = [f for f in os.listdir(self.description_dir) if int(f.split("_")[1]) == n_shapes]

        self.qa_dir = os.path.join(dir, qa_dir)
        self.qa_files = [f for f in os.listdir(self.qa_dir) if int(f.split("_")[1]) == n_shapes]

        self.description_files.sort()
        self.qa_files.sort()

        print(self.description_files)
        print(self.qa_files)
        if len(self.qa_files) != len(self.description_files):
            raise ValueError



    def __len__(self):
        return len(self.qa_files)


    def __getitem__(self, idx):
        with open(f"{self.description_dir}/{self.description_files[idx]}", "r") as file:
            description = json.load(file)
        with open(f"{self.qa_dir}/{self.qa_files[idx]}", "r") as file:
            qa = json.load(file)

        if len(qa["transitivity"]) == 0:
            return None, None, None

        ix = random.randint(0, 47)
        return description["partial"], qa["existence"][ix][0], qa["existence"][ix][1]
