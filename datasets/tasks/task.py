import json
from itertools import product

from datasets.constants import SHAPES, COLORS, SIZES

class Task:

    def __init__(self, name):
        self.name = name

    def generate_questions(self, shapes, selected_answer=None):
        raise NotImplementedError()


    def select_expected_answer(self, n_current, n_total):
        return None

    def score(self, filepath):
        with open(filepath, "r") as file:
            result = json.load(file)

        return 1 if str(result["expected"]).lower() in str(result["actual"]).lower() else 0

    # Helpful utility methods
    def _generate_attributes(self):
        class AttributeGenerator:
            def __init__(self):
                self.iterable = product(list(SHAPES) + [None], list(SIZES) + [None], list(COLORS) + [None])

            def __iter__(self):
                return self

            def __next__(self):
                next_item = next(self.iterable)
                if next_item != (None, None, None):
                    return next_item
                raise StopIteration()

        return AttributeGenerator()
