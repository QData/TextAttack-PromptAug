import json
import random
import sys
import os

from shapes import Shape
from constants import SHAPES, SIZES, COLORS
from utils import get_relationships, json_to_shapes

class QuestionGenerator:
    
    def __init__(self, shapes):
        self.shapes = shapes
        self.relationships = get_relationships(self.shapes)


    @classmethod
    def from_file(cls, filename):
        return cls(json_to_shapes(filename))


    def generate_questions(self):
        return {
            "existence": self.generate_existence_questions(), 
            "transitivity": self.generate_transitivity_questions(),
        }
    
    
    def existence(self, shape_value=None, color_value=None, size_value=None):
        for shape in self.shapes:
            if shape_value is None or shape.name == shape_value:
                if color_value is None or shape.color == color_value:
                    if size_value is None or shape.size == size_value:
                        return True
        return False


    def generate_transitivity_questions(self):
        """
        Generates two transitvity questions, one for horizontal directions and
        one for vertical directions

        """
        results = {
            "horizontal": [], 
            "vertical": []
        }

        # We need at least 3 shapes for transitivity
        if len(self.shapes) < 3:
            return results


        def valid(candidate, direction):
            if direction == "horizontal":
                return (
                    len(self.relationships[candidate]["Left"]) > 1,
                    len(self.relationships[candidate]["Right"]) > 1
                )
            # direction == vertical
            return (
                len(self.relationships[candidate]["Above"]) > 1,
                len(self.relationships[candidate]["Below"]) > 1
            )


        for direction in results.keys():
            tries = 0
            candidate = random.randint(0, len(self.shapes) - 1)
            found1, found2 = valid(candidate, direction)

            # This condition may never be satisfied, so limit the number of tries
            while not (found1 or found2) and tries < (4 * len(self.shapes)):
                candidate = random.randint(0, len(self.shapes) - 1)
                found1, found2 = valid(candidate, direction)

                tries += 1

            if tries == 4 * len(self.shapes):
                continue

            if direction == "horizontal":
                # There are at least two shapes on the left, so this is the right object
                if found1:
                    right = self.shapes[candidate]
                    # Pick a random object in the relationship list so that at least 1 object is in between
                    left = self.shapes[self.relationships[candidate]["Left"][random.randint(1, len(self.relationships[candidate]["Left"]) - 1)]]
                else:
                    left = self.shapes[candidate]
                    right = self.shapes[self.relationships[candidate]["Right"][random.randint(1, len(self.relationships[candidate]["Right"]) - 1)]]

                question = f"Where is the {left} relative to the {right}?"
                answer = "Left"
                results[direction].append((question, answer))

                question = f"Where is the {right} relative to the {left}?"
                answer = "Right"
                results[direction].append((question, answer))

            # Corresponds to above
            else:
                # There are at least two shapes above this one, so it is the bottom
                if found1:
                    bottom = self.shapes[candidate]
                    top = self.shapes[self.relationships[candidate]["Above"][random.randint(1, len(self.relationships[candidate]["Above"]) - 1)]]
                else:
                    top = self.shapes[candidate]
                    bottom = self.shapes[self.relationships[candidate]["Below"][random.randint(1, len(self.relationships[candidate]["Below"]) - 1)]]

                question = f"Where is the {top} relative to the {bottom}?"
                answer = "Above"
                results[direction].append((question, answer))

                question = f"Where is the {bottom} relative to the {top}?"
                answer = "Below"
                results[direction].append((question, answer))

        return results

    
    def generate_existence_questions(self):
        """
        Generate every existence question for the shapes.

        Note this always generates 47 question answer pairs

        """
        qa = []
        
        # Single Attribute
        for shape_type in SHAPES:
            qa.append((
                f"Is there a {shape_type.lower()}?", 
                "Yes" if self.existence(shape_value=shape_type) else "No"
            ))
        for color in COLORS:
            qa.append((
                f"Is there a shape that is {color.lower()}?", 
                "Yes" if self.existence(color_value=color) else "No"
            ))
        for size in SIZES:
            qa.append((
                f"Is there a {size.lower()} shape?",
                "Yes" if self.existence(size_value=size) else "No"
            ))

        # Double Attribute
        for shape_type in SHAPES:
            for color in COLORS:
                qa.append((
                    f"Is there a {color.lower()} {shape_type.lower()}?", 
                    "Yes" if self.existence(shape_value=shape_type, color_value=color) else "No"
                ))
            for size in SIZES:
                qa.append((
                    f"Is there a {size.lower()} {shape_type.lower()}?", 
                    "Yes" if self.existence(shape_value=shape_type, size_value=size) else "No"
                ))
        for color in COLORS:
            for size in SIZES:
                qa.append((
                    f"Is there a {size.lower()} {color.lower()} shape?",
                    "Yes" if self.existence(color_value=color, size_value=size) else "No"
                ))

        # Triple Attribute
        for shape_type in SHAPES:
            for color in COLORS:
                for size in SIZES:
                    qa.append((
                        f"Is there a {size.lower()} {color.lower()} {shape_type.lower()}?", 
                        "Yes" if self.existence(shape_value=shape_type, color_value=color, size_value=size) else "No"
                    ))
            
        return qa


if __name__ == "__main__":
    SEED = 37
    DATA_ROOT = "data/questions"

    random.seed(SEED)
    if len(sys.argv) != 3:
        print("Usage: python question_generator.py <number of shapes in canvas> <number of example canvases>")
        exit()

    n_shapes, n_examples = map(int, sys.argv[1:])
    print(f"Generating questions for {n_examples} examples with {n_shapes} shape(s).")

    if not os.path.isdir(DATA_ROOT):
        os.makedirs(DATA_ROOT)

    for i in range(0, n_examples):
        gen = QuestionGenerator.from_file(f"data/canvases/canvas_{n_shapes}_{i}.json")
        qa = gen.generate_questions()

        with open(f"{DATA_ROOT}/canvas_{n_shapes}_{i}.json", "w") as file:
            json.dump(qa, file, indent=4)

