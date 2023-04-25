import json
import random

from datasets.tasks.task import Task
from datasets.constants import SHAPES

class ShuffleTrackingTask(Task):

    def __init__(self, name,):
        super().__init__(name)


    def _generate_description(self, direction_type, shapes):
        description = f"There are {len(shapes)} shapes in a canvas. "
        if direction_type == "horizontal":
            if random.random() < 0.5:
                description += "From left to right, the shapes are "
            else:
                description += "From right to left, the shapes are "
                shapes = shapes[::-1]
        if direction_type == "vertical":
            if random.random() < 0.5:
                description += "From top to bottom, the shapes are "
                shapes = shapes[::-1]
            else:
                description += "From bottom to top, the shapes are "
                

        for i, shape in enumerate(shapes):
            if i + 1 == len(shapes):
                description += f"a {shape}. "
            elif i + 2 == len(shapes):
                description += f"a {shape}, and "
            else:
                description += f"a {shape}, "

        return description


    def generate_questions(self, shapes, selected_answer=None):
        """
        Generate every counting question for the shapes

        """
        qa = []
        if len(shapes) < 2:
            return qa

        if random.random() < 0.5:
            direction_type = "horizontal"
            shapes = sorted(shapes, key=lambda shape: shape.center[0])
        else:
            direction_type = "vertical"
            shapes = sorted(shapes, key=lambda shape: shape.center[1])

        description = self._generate_description(direction_type, shapes)

        last_swap = set()
        for _ in range(0, len(shapes)):
            shape1_index = random.randint(0, len(shapes) - 1)
            shape2_index = random.randint(0, len(shapes) - 1)

            # Don't swap a shape with itself and don't repeat the last swap
            while shape1_index == shape2_index or (shape1_index in last_swap and shape2_index in last_swap):
                shape1_index = random.randint(0, len(shapes) - 1)
                shape2_index = random.randint(0, len(shapes) - 1)

            last_swap = {shape1_index, shape2_index}

            description += f"The {shapes[shape1_index]} and the {shapes[shape2_index]} swap positions. "
            shapes[shape1_index], shapes[shape2_index] = shapes[shape2_index], shapes[shape1_index]

        self.description = description

        # There are probably better ways to do this,
        # but its easy for small numbers and works
        nth = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
            5: "fifth",
            6: "sixth", 
            7: "seventh", 
            8: "eigth", 
            9: "ninth",
        }

        asked = set()
        for _ in range(0, 3):
            if direction_type == "horizontal":
                if random.random() < 0.5:
                    origin = "left"
                else:
                    origin = "right"
            else:
                if random.random() < 0.5:
                    origin = "top"
                else:
                    origin = "bottom"

            # The shapes are sorted left to right or bottom to top
            # convert position relative to the origin to
            # the index matching this sort
            def position_to_index(position):
                if origin == "right" or origin == "top":
                    return len(shapes) - position - 1
                return position

            position = random.randint(0, len(shapes) - 1)
            while shapes[position_to_index(position)] in asked:
                position = random.randint(0, len(shapes) - 1)
            asked.add(shapes[position_to_index(position)])

            qa.append((
                f"What shape is {nth[position + 1]} from the {origin}?", 
                str(shapes[position_to_index(position)])
            ))

        return qa


    def score(self, filepath):
        with open(filepath, "r") as file:
            result = json.load(file)
        expected = str(result["expected"]).lower()
        actual = str(result["actual"]).lower()
        score = 0

        # Score only the first shape mentioned
        index = len(actual)
        for shape in SHAPES:
            new_index = actual.find(shape.lower()) 
            if new_index != -1:
                index = min(index, new_index + len(shape))
        actual = actual[:index + 1]

        return 1 if expected in actual else 0
