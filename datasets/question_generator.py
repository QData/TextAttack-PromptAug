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

        This depends on the prompt

        """

        # We need at least 3 shapes for transitivity
        if len(self.shapes) < 3:
            return []

        tries = 0
        start = random.randint(0, len(self.shapes) - 1)
        found_left = len(self.relationships[start]["Left"]) > 1
        found_right = len(self.relationships[start]["Right"]) > 1
        # This condition may never be satisfied, so limit the number of tries
        while not (found_left or found_right) and tries < (2 * len(self.shapes)):
            start = random.randint(0, len(self.shapes) - 1)
            found_left = len(self.relationships[start]["Left"]) > 1
            found_right = len(self.relationships[start]["Right"]) > 1

            tries += 1

        if tries == 2 * len(self.shapes):
            return []

        # There are at least two shapes on the left, so this is the right object
        if found_left:
            right = self.shapes[start]
            # Pick a random object in the relationship list so that at least 1 object is in between
            left = self.shapes[self.relationships[start]["Left"][random.randint(1, len(self.relationships[start]["Left"]) - 1)]]
        else:
            left = self.shapes[start]
            right = self.shapes[self.relationships[start]["Right"][random.randint(1, len(self.relationships[start]["Right"]) - 1)]]

        if random.random() < 0.5:
            question = f"Where is the {left} relative to the {right}?"
            answer = "Left"
        else:
            question = f"Where is the {right} relative to the {left}?"
            answer = "Right"

        return [(question, answer)]
    
    
    def generate_transitivity_promopt(self, horizontal=True):
        """
        Simple transitivity prompt for 3 objects

        """
        if len(self.shapes) != 3:
            return []

        description = "There are 3 shapes in a canvas. "
        if horizontal:
            i = random.randint(0, len(self.shapes) - 1)
            start = self.shapes[i]

            description += f"A {start} is in the canvas. "
            # The ordering can be A B C
            # Right shape, corresponds to C 
            if len(self.relationships[i]["Left"]) == 2:
                first = self.shapes[min(self.relationships[i]["Left"], key=lambda i: self.shapes[i].center[0])]
                second = self.shapes[max(self.relationships[i]["Left"], key=lambda i: self.shapes[i].center[0])]
                direction1 = "To the left"
                direction2 = "To the left"

                left = first
                right = start

            # Left shape, corresponds to A
            elif len(self.relationships[i]["Right"]) == 2:
                first = self.shapes[min(self.relationships[i]["Right"], key=lambda i: self.shapes[i].center[0])]
                second = self.shapes[max(self.relationships[i]["Right"], key=lambda i: self.shapes[i].center[0])]
                direction1 = "To the right"
                direction2 = "To the right"

                left = start
                right = second

            # Middle shape, corresponds to B
            elif len(self.relationships[i]["Left"]) == 1 and len(self.relationships[i]["Right"]) == 1:
                first = self.shapes[self.relationships[i]["Left"][0]]
                second = self.shapes[self.relationships[i]["Right"][0]]
                direction1 = "To the left"
                direction2 = "To the right"

                left = first
                right = second
            else:
                direction1 = "ERROR"
                direction2 = "ERROR"
                first = "ERROR"
                second = "ERROR"
                left = "ERROR"
                right = "ERROR"
                

            description += f"{direction1} of the {start} is a {first}. "
            description += f"{direction2} of the {start} is a {second}. "

            description += "\nQuestion: "
            if random.random() < 0.5:
                description += f"Where is the {left} relative to the {right}? "
                answer = "Left"
            else:
                description += f"Where is the {right} relative to the {left}? "
                answer = "Right"

        else:
            pass


        return description, answer
        
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

