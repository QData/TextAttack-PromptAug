import json
import random

from datasets.utils import get_relationships
from datasets.tasks.task import Task

class TransitivityTask(Task):

    def __init__(self, name):
        super().__init__(name)


    def _generate_description(self, shapes, relationships, origin_shape_index, direction_type):
        origin_shape = shapes[origin_shape_index]
        description = f"There are {len(shapes)} shapes in a canvas. There is a {origin_shape} in the canvas. "
        if direction_type == "horizontal":
            directions = ["Left", "Right"]
        else:
            directions = ["Above", "Below"]
        random.shuffle(directions)
        
        for direction in directions:
            prev_shape = origin_shape
            for next_shape_index in relationships[origin_shape_index][direction]:
                next_shape = shapes[next_shape_index]
                if direction_type == "horizontal":
                    description += f"To the {direction.lower()} of the {prev_shape} is a {next_shape}. "
                else:
                    description += f"{direction} the {prev_shape} is a {next_shape}. "
                prev_shape = next_shape

        self.description = description


    def generate_questions(self, shapes, selected_answer=None):
        qa = []

        # Need at least 3 shapes for transitivity
        if len(shapes) < 3:
            return qa

        # Pick one shape as the origin shape
        relationships = get_relationships(shapes)

        # TODO: This could loop indefinetly, but hasn;t been an issue yet...
        # Consider a large shape at (0, 0), a small shape at (0, 5), and a small shape
        # at (5, 0)
        while True:
            origin_shape_index = random.randint(0, len(shapes) - 1)

            possible_directions = []
            if len(relationships[origin_shape_index]["Left"]) + len(relationships[origin_shape_index]["Right"]) > 1:
                possible_directions.append("horizontal")
            if len(relationships[origin_shape_index]["Above"]) + len(relationships[origin_shape_index]["Below"]) > 1:
                possible_directions.append("vertical")
            
            if len(possible_directions) != 0:
                break

        direction_type = random.choice(possible_directions)        
        self._generate_description(shapes, relationships, origin_shape_index, direction_type)

        # Pick two shapes, make sure they are not directly next to each other 
        # and that they do not have the same coordinates
        found = False
        while not found:
            shape1_index, shape2_index = random.sample(range(0, len(shapes)), 2)
            found = True
            if direction_type == "horizontal":
                # Shape 2 is directly to the left of shape 1
                if len(relationships[shape1_index]["Left"]) > 0 and relationships[shape1_index]["Left"][0] == shape2_index:
                    found = False
                # Shape 2 is directly to the right of shape 1
                elif len(relationships[shape1_index]["Right"]) > 0 and relationships[shape1_index]["Right"][0] == shape2_index:
                    found = False
                elif shapes[shape1_index].center[0] == shapes[shape2_index].center[0]:
                    found = False
            else:
                # Shape 2 is directly above shape 1
                if len(relationships[shape1_index]["Above"]) > 0 and relationships[shape1_index]["Above"][0] == shape2_index:
                    found = False
                # Shape 2 is directly below shape 1
                elif len(relationships[shape1_index]["Below"]) > 0 and relationships[shape1_index]["Below"][0] == shape2_index:
                    found = False
                elif shapes[shape1_index].center[1] == shapes[shape2_index].center[1]:
                    found = False

        def get_answer(shape1_index, shape2_index):
            if direction_type == "horizontal":
                answer = "Left" if shape2_index in relationships[shape1_index]["Left"] else "Right"
            else:
                answer = "Above" if shape2_index in relationships[shape1_index]["Above"] else "Below"
            return answer

        qa.append((
            f"Where is the {shapes[shape2_index]} relative to the {shapes[shape1_index]}?",
            get_answer(shape1_index, shape2_index)
        ))

        used = {(shape1_index, shape2_index)}

        # For the few shot questions, there may be no pairs left that are not 
        # directly next to each other, so just choose two shapes
        # Not that there may not exist any pair of shapes that satisfy this condition
        # so limit the number of attempts
        for _ in range(0, 2):

            attempts = 0
            found = False
            while not found:
                shape1_index, shape2_index = random.sample(range(0, len(shapes)), 2)

                found = True
                if (shape1_index, shape2_index) in used or (shape2_index, shape1_index) in used:
                    found = False
                # Edge case: No horizontal relationship between two objects (e.g. same x coordinate)
                elif direction_type == "horizontal" and shape1_index not in relationships[shape2_index]["Left"] and shape1_index not in relationships[shape2_index]["Right"]:
                    found = False
                # Edge case: No vertical relationship between two objects (e.g. same y coordinate)
                elif direction_type == "vertical" and shape1_index not in relationships[shape2_index]["Above"] and shape1_index not in relationships[shape2_index]["Below"]:
                    found = False

                if attempts > 5 * len(shapes) ** 2:
                    break
                attempts += 1

            if not found:
                continue

            qa.append((
                f"Where is the {shapes[shape2_index]} relative to the {shapes[shape1_index]}?",
                get_answer(shape1_index, shape2_index)
            ))
            used.add((shape1_index, shape2_index))

        return qa


    def score(self, filepath):
        with open(filepath, "r") as file:
            result = json.load(file)
        expected = str(result["expected"]).lower()
        actual = str(result["actual"]).lower()
        score = 0

        # Process only the first line that contains directional information
        found = False
        directions = ["left", "right", "above", "below"]
        lines = actual.split("\n")
        for line in lines:
            for direction in directions:
                if direction in line:
                    actual = line
                    found = True
            if found:
                break
            
        # Filter out strings like "There is not enough information"
        if "no " in actual or "not " in actual:
            return score

        # Score is 1 for a correct answer
        choices = ["left", "right", "above", "below"]
        for word in actual.split():
            if word in choices:
                if word == expected:
                    score += 1
                else:
                    score -= 0.5

        return max(0, score)
