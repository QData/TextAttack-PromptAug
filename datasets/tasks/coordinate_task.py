import json
import random

from datasets.utils import get_relationships
from datasets.tasks.task import Task

class CoordinateTask(Task):

    def __init__(self, name,):
        super().__init__(name)


    def generate_questions(self, shapes, selected_answer=None):
        """
        Generates a question asking the positional relationship
        between every pair of objects

        """
        qa = []
        relationships = get_relationships(shapes)
        for i in range(0, len(shapes) - 1):
            for j in range(i + 1, len(shapes)):
                answer = ""
                if j in relationships[i]["Above"]:
                    answer += "Above "
                elif j in relationships[i]["Below"]:
                    answer += "Below "

                if j in relationships[i]["Left"]:
                    answer += "Left"
                if j in relationships[i]["Right"]:
                    answer += "Right"

                qa.append((
                    f"Where is the {shapes[j]} relative to the {shapes[i]}?",
                    answer
                ))

        n_pairs = len(shapes) * (len(shapes) - 1) // 2
        return random.sample(qa, min(3, n_pairs))
