import json
import random

from datasets.tasks.task import Task

class CountTask(Task):

    def __init__(self, name,):
        super().__init__(name)


    def count(self, shapes, shape_type=None, color=None, size=None):
        count = 0
        for shape in shapes:
            if shape_type is not None and shape.name != shape_type:
                continue
            if color is not None and shape.color != color:
                continue
            if size is not None and shape.size != size:
                continue
            count += 1

        return count


    def select_expected_answer(self, n_current, n_examples):
        return 0 if n_current < (n_examples // 4) else -1


    def generate_questions(self, shapes, selected_answer=None):
        """
        Generate every counting question for the shapes

        """
        qa = []

        for shape, size, color in self._generate_attributes():
            if shape:
                qa.append((
                    f"How many {size.lower() + ' ' if size else ''}{color.lower() + ' ' if color else ''}{shape.lower()}s are there?",
                    self.count(shapes, shape, color, size)
                ))
            else:
                qa.append((
                    f"How many {size.lower() + ' ' if size else ''}{color.lower() + ' ' if color else ''}shapes are there?",
                    self.count(shapes, shape, color, size)
                ))

        if selected_answer is None:
            return random.sample(qa, 3)

        if selected_answer == 0:
            selection = random.choice(
                [(question, answer) for question, answer in qa if answer == selected_answer]
            )
        else:
            selection = random.choice(
                [(question, answer) for question, answer in qa if answer != 0]
            )

        few_shot_questions = random.sample(
            [(question, answer) for question, answer in qa if question != selection[0]], 
            2
        )

        return [selection] + few_shot_questions
