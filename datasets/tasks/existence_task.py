import json
import random

from datasets.tasks.task import Task

class ExistenceTask(Task):

    def __init__(self, name,):
        super().__init__(name)


    def existence(self, shapes, shape_value=None, color_value=None, size_value=None):
        for shape in shapes:
            if shape_value is None or shape.name == shape_value:
                if color_value is None or shape.color == color_value:
                    if size_value is None or shape.size == size_value:
                        return True
        return False


    def select_expected_answer(self, n_current, n_examples):
        return "Yes" if n_current < (n_examples // 2) else "No"


    def generate_questions(self, shapes, selected_answer=None):
        qa = []

        for shape, size, color in self._generate_attributes():
            # Only asking about color
            if shape is None and size is None:
                qa.append((
                    f"Is there a shape that is {color.lower()}?",
                    "Yes" if self.existence(shapes, shape, color, size) else "No"
                ))
            # Asking about size or size and color
            elif shape is None:
                qa.append((
                    f"Is there a {size.lower()} {color.lower() + ' ' if color else ''}shape?",
                    "Yes" if self.existence(shapes, shape, color, size) else "No"
                ))
            else:
                qa.append((
                    f"Is there a {size.lower() + ' ' if size else ''}{color.lower() + ' ' if color else ''}{shape.lower()}?",
                    "Yes" if self.existence(shapes, shape, color, size) else "No"
                ))

        if selected_answer is None:
            return random.sample(qa, 3)

        selection = random.choice(
            [(question, answer) for question, answer in qa if answer == selected_answer]
        )
        few_shot_questions = random.sample(
            [(question, answer) for question, answer in qa if question != selection[0]], 
            2
        )

        return [selection] + few_shot_questions
