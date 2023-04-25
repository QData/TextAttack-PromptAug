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
   
        n_pairs = len(qa)
        return random.sample(qa, min(3, n_pairs))


    def score(self, filepath):
        with open(filepath, "r") as file:
            result = json.load(file)

        actual = str(result["actual"]).lower()
        expected = str(result["expected"]).lower()

        # Models may generate multiple answers as part of
        # generation, take the first one
        for token in ["answer:", "a:"]:
            if token in actual:
                actual = actual.split(token)
                if len(actual) > 1:
                    actual = actual[1]
                else:
                    actual = actual[0]
                break

        # The answer may be an x and a y direction, give 0.5 for each
        # or one if only one direction is correct
        # and subtract for other answers
        directions = {"left", "right", "above", "below"}
        answers = expected.split()
        score = 0

        if len(answers) == 1:
            increment = 1
        else:
            increment = 0.5

        for word in actual.split():
            if word in directions:
                if word in answers:
                    score += increment
                else:
                    score -= 0.5

        return max(0, score)