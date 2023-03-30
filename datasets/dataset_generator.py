import json
import sys
import os
import random
import numpy as np

from shape_generator import generate_shapes
from description_generator import DescriptionGenerator
from question_generator import QuestionGenerator


if __name__ == "__main__":
    if __name__ == "__main__":
        SEED = 37
        DATA_ROOT = "data"

        random.seed(SEED)
        if len(sys.argv) != 3:
            print("Usage: python data_generator.py <number of shapes in canvas> <number of example canvases>")
            exit()

        n_shapes, n_examples = map(int, sys.argv[1:])
        print(f"Generating {n_examples} examples with {n_shapes} shape(s).")

    if not os.path.isdir(DATA_ROOT):
        os.makedirs(DATA_ROOT)

    # Transitive answer counts: Left, Right, Above, Below
    counts = [0, 0, 0, 0]
    for i in range(0, n_examples):
        shapes = generate_shapes(n_shapes)

        description_gen = DescriptionGenerator(shapes)
        question_gen = QuestionGenerator(shapes)

        # Generate descriptions
        descriptions = description_gen.generate_descriptions()

        # Generate questions
        questions = question_gen.generate_questions()

        # Choose one of each question type, make a balanced dataset
        # Existence
        selected_answer = "Yes" if i < (n_examples // 2) else "No"
        questions["existence"] = random.choice(
            [(question, answer) for question, answer in questions["existence"] if answer == selected_answer]
        )

        # Transitvity
        if n_shapes < 3:
            del questions["transitivity"]
            del descriptions["transitive"]
        else:
            # Round robin the answer, try to make a balanced dataset
            min_ix = np.argmin(counts)

            # Edge cases where this canvas doesn't have horizontal or vertical 
            # transitivity but we tried to select that one
            if min_ix < 2 and (descriptions["transitive"]["left"] is None and descriptions["transitive"]["right"] is None) or len(questions["transitivity"]["horizontal"]) == 0:
                min_ix = np.argmin(counts[2:]) + 2
            if min_ix >= 2 and descriptions["transitive"]["above"] is None and descriptions["transitive"]["below"] is None or len(questions["transitivity"]["vertical"]) == 0:
                min_ix = np.argmin(counts[:2])

            # Horizontal Direction
            if min_ix < 2:
                try:
                    questions["transitivity"] = questions["transitivity"]["horizontal"][min_ix]
                except:
                    print([shape.to_json() for shape in shapes])
                    print()
                    print(descriptions)
                    print()
                    print(questions)
                    break
                if descriptions["transitive"]["left"] is None:
                    descriptions["transitive"] = descriptions["transitive"]["right"]
                elif descriptions["transitive"]["right"] is None or random.random() < 0.5:
                    descriptions["transitive"] = descriptions["transitive"]["left"]
                else:
                    descriptions["transitive"] = descriptions["transitive"]["right"]
            # Vertical Direction
            else:
                questions["transitivity"] = questions["transitivity"]["vertical"][min_ix - 2]
                if descriptions["transitive"]["above"] is None:
                    descriptions["transitive"] = descriptions["transitive"]["below"]
                elif descriptions["transitive"]["below"] is None or random.random() < 0.5:
                    descriptions["transitive"] = descriptions["transitive"]["above"]
                else:
                    descriptions["transitive"] = descriptions["transitive"]["below"]

            counts[min_ix] += 1

        
        # Done processing
        # Write out the results
        with open(f"data/canvas_{n_shapes}_{i}.json", "w") as file:
            data = {
                "canvas": [shape.to_json() for shape in shapes],
                "descriptions": descriptions, 
                "questions": questions
            }
            json.dump(data, file, indent=4)


    print("Done")
    print()
    print(f"Existence Answer Counts (Y, N): {n_examples // 2}, {n_examples - (n_examples // 2)}")
    print(f"Transitivity Answer Counts (L, R, A, B): {counts}")

