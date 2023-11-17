import sys
import os
import json

from utils import json_to_shapes

from datasets.description_generator import DescriptionGenerator
from datasets.shape_generator import generate_shapes
from datasets.tasks.registered_tasks import tasks


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python data_generator.py <number of shapes in canvas> <number of example canvases>")
        exit()

    DATA_ROOT = "data"

    n_shapes, n_examples = map(int, sys.argv[1:])
    print(f"Generating {n_examples} examples with {n_shapes} shape(s).")

    if not os.path.isdir(DATA_ROOT):
        os.makedirs(DATA_ROOT)


    for i in range(0, n_examples):
        filepath = f"{DATA_ROOT}/canvas_{n_shapes}_{i}.json"
        # If data already exists, we just want to update it
        if os.path.isfile(filepath):
            shapes = json_to_shapes(filepath)
        # Otherwise, generate a new canvas
        else:
            shapes = generate_shapes(n_shapes)

        data = {
            "canvas": [shape.to_json() for shape in shapes],
            "descriptions": DescriptionGenerator(shapes).generate_descriptions(), 
            "questions": {}
        }
        for task in tasks:
            selected_answer = task.select_expected_answer(i, n_examples)
            task_qa = task.generate_questions(shapes, selected_answer)
            if len(task_qa) != 0:
                data["questions"][task.name] = task_qa

                # Some tasks generate their own descriptions or additional
                # information to add to the description
                if hasattr(task, "description"):
                    data["descriptions"][task.name] = task.description


        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                old = json.load(file)

            # Add all the keys in old to data, same keys are overwritten by old values
            # First, update the questions sub-dictionary in old with the new questions
            old["questions"] = data["questions"] | old["questions"]
            old["descriptions"] = data["descriptions"] | old["descriptions"]
            # Then update all the main keys
            data = data | old

        # Write out the new data
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
