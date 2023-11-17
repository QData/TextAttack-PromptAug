import json
import random

from itertools import product

from datasets.constants import SHAPES, COLORS, SIZES
from datasets.shapes import Shape
from datasets.tasks.task import Task


class ExistenceTrackingTask(Task):

    def __init__(self, name,):
        super().__init__(name)

    
    def select_expected_answer(self, n_current, n_examples):
        return "Yes" if n_current < (n_examples // 2) else "No"


    def generate_questions(self, shapes, selected_answer=None):
        qa = []

        in_canvas = set(shapes)
        not_in_canvas = set()

        shape_choices = list(product(SHAPES, COLORS, SIZES))
        shape_choices = [Shape.get_constructor(attr[0])(attr[1], attr[2], (0, 0)) for attr in shape_choices]
        random.shuffle(shape_choices)

        i = 0

        question = ""
        for _ in range(0, len(shapes)):
            if len(in_canvas) == 1 or random.random() < 0.6667:
                while shape_choices[i] in in_canvas:
                    i = (i + 1) % len(shape_choices)
                question += f"A {shape_choices[i]} is added to the canvas. "
                in_canvas.add(shape_choices[i])
                if shape_choices[i] in not_in_canvas:
                    not_in_canvas.remove(shape_choices[i])
                i = (i + 1) % len(shape_choices)
            else:
                to_remove = random.choice(list(in_canvas))
                question += f"The {to_remove} is removed from the canvas. "
                in_canvas.remove(to_remove)
                not_in_canvas.add(to_remove)

        self.description = question
       

        if len(not_in_canvas) > 0:
            missing_shape = random.choice(list(not_in_canvas))
        else:
            while shape_choices[i] in in_canvas:
                i = (i + 1) % len(shape_choices)
            missing_shape = shape_choices[i]
        missing_shape_question = (
             f"Is there a {missing_shape} in the canvas? ", 
            "No"
        )

        existing_shape = random.choice(list(in_canvas))
        existing_shape_question = (
            f"Is there a {existing_shape} in the canvas? ", 
            "Yes"
        )

        
        qa.append(existing_shape_question)
        qa.append(missing_shape_question)
        
        if selected_answer is None:
            qa.shuffle()
        if selected_answer == "No":
            # Reverse the list so the first question is the missing shape question
            qa = qa[::-1]

        # Last few shot question
        if random.random() < 0.5:
            in_canvas.remove(existing_shape)
            qa.append((
                f"Is there a {random.choice(list(in_canvas))} in the canvas? ", 
                "Yes"
            ))
        else:
            if len(not_in_canvas) > 1:
                not_in_canvas.remove(missing_shape)
                missing_shape = random.choice(list(not_in_canvas))
            else:
                while shape_choices[i] in in_canvas:
                    i = (i + 1) % len(shape_choices)
                missing_shape = shape_choices[i]
            
            qa.append((
                f"Is there a {missing_shape} in the canvas? ", 
                "No"
            ))
            
        return qa