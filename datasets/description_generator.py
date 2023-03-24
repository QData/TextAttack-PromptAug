import sys
import os
import random
import json

from utils import json_to_shapes, get_relationships


class DescriptionGenerator:

    def __init__(self, shapes):
        self.shapes = shapes
        self.relationships = get_relationships(shapes)
        self.filename = None


    @classmethod
    def from_file(cls, filename):
        obj = cls(json_to_shapes(filename))
        obj.filename = filename.split("/")[-1]
        return obj


    def generate_descriptions(self, method="short"):
        if method not in {"full", "short", "transitive"}:
            raise ValueError(f"The method, {method}, provided is not supported.")

        name_to_function = {
            "full": self._full, 
            "partial": self._partial,
            "short": self._short, 
            "transitive": self._transitive
        }

        results = {}
        for name, function in name_to_function.items():
            try:
                results[name] = function()
            except NotImplementedError:
                pass
                
        with open(f"{DATA_ROOT}/{self.filename}", "w") as file:
            json.dump(results, file, indent=4)


    def get_direction(self, origin_shape_ix, other_shape_ix):
        x_dir, y_dir = None, None
        if other_shape_ix in self.relationships[origin_shape_ix]["Left"]:
            x_dir = "Left"
        elif other_shape_ix in self.relationships[origin_shape_ix]["Right"]:
            x_dir = "Right"

        if other_shape_ix in self.relationships[origin_shape_ix]["Above"]:
            y_dir = "Above"
        elif other_shape_ix in self.relationships[origin_shape_ix]["Below"]:
            y_dir = "Below"

        return x_dir, y_dir


    def _full(self):
        """
        Describe the relationship of every object to every other object
        For n objects, we get n(n - 1) relations

        """
        if len(self.shapes) == 1:
            description = f"There is {len(self.shapes)} shape in a canvas. "
        else:
            description = f"There are {len(self.shapes)} shapes in a canvas. "
        
        for i, shape in enumerate(self.shapes):
            description += f"There is a {shape} in the canvas. "

            for j, other in enumerate(self.shapes):
                if i == j:
                    continue

                x_dir, y_dir = self.get_direction(i, j)

                if x_dir and y_dir:
                    direction = f"to the {y_dir.lower()} {x_dir.lower()}"
                elif x_dir:
                    direction = f"{x_dir.lower()} of"
                else:
                    direction = y_dir.lower()
                    
                description += f"A {self.shapes[j]} is {direction} this {shape}. "
        return description


    def _partial(self):
        """
        Describe the relationship between every pair of objects exactly once
        For n objects, we get n(n - 1)/2 relations

        """
        if len(self.shapes) == 1:
            description = f"There is {len(self.shapes)} shape in a canvas. "
        else:
            description = f"There are {len(self.shapes)} shapes in a canvas. "
        
        for i, shape in enumerate(self.shapes):
            description += f"There is a {shape} in the canvas. "

            for j, other in enumerate(self.shapes[i + 1:]):
                x_dir, y_dir = self.get_direction(i, j + i + 1)

                if x_dir and y_dir:
                    direction = f"to the {y_dir.lower()} {x_dir.lower()}"
                elif x_dir:
                    direction = f"{x_dir.lower()} of"
                else:
                    direction = y_dir.lower()
                    
                description += f"A {self.shapes[j]} is {direction} this {shape}. "
        return description


    def _short(self):
        """
        Describe the relative relationship of an object to exactly one other object
        For n objects, we get n - 1 relations

        """
        raise NotImplementedError

    
    def _transitive(self):
        """
        Simple transitivity prompt for 3 objects

        1 2 3

        1 -> 2 -> 3
        3 -> 2 -> 1
        2 -> 1, 2 -> 3

        """
        horizontal = True
        if len(self.shapes) < 3:
            return ""
        if len(self.shapes) != 3:
            raise NotImplementedError


        # TODO: Fix me, there could be two objects to the left (or right) with the same x coordinate
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
                return ""

            description += f"{direction1} of the {start} is a {first}. "
            description += f"{direction2} of the {start} is a {second}. "
        else:
            description = ""


        return description


if __name__ == "__main__":
    DATA_ROOT = "data/descriptions"

    if len(sys.argv) != 3:
        print("Usage: python description_generator.py <number of shapes in canvas> <number of example canvases>")
        exit()

    n_shapes, n_examples = map(int, sys.argv[1:])
    print(f"Generating descriptions for the first {n_examples} examples with {n_shapes} shape(s).")

    if not os.path.isdir(DATA_ROOT):
        os.makedirs(DATA_ROOT)

    for i in range(0, n_examples):
        gen = DescriptionGenerator.from_file(f"data/canvases/canvas_{n_shapes}_{i}.json")
        gen.generate_descriptions()


