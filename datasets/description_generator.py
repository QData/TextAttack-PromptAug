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
        result = {}
        for method in ["left", "right", "above", "below"]:
            result[method] = self._transitive_helper(method)
        return result


    def _transitive_helper(self, method="left"):
        """
        Describe every object in order of method. For example, for method='left',
        describe all the objects, starting with the rightmost one and moving left.

        For n objects, we get n - 1 relations.

        """

        if method not in {"left", "right", "above", "below"}:
            raise ValueError(f"{method} is not a valid method")

        def compare(shape1, shape2):
            # We want the rightmost object so there are objects to the left
            if method == "left":
                return shape1.right > shape2.right
            # We want the leftmost object so there are objects to the right
            if method == "right":
                return shape1.left < shape2.left
            # We want the bottommost object so there are objects above
            if method == "above":
                return shape1.bottom < shape2.bottom
            # method == "below"
            return shape1.top > shape2.top


        # Find the first object
        start = 0
        for i in range(1, len(self.shapes)):
            if compare(self.shapes[i], self.shapes[start]):
                start = i

        # Check there are at least 2 objects in the direction
        if len(self.relationships[start][method.title()]) < 2:
            return None

        # Iterate over the objects in order and add them to the description
        description = f"There is a {self.shapes[start]} in the canvas. "
        prev = start
        for i in self.relationships[start][method.title()]:
            if method in {"left", "right"}:
                description += f"To the {method} of {self.shapes[prev]} is a {self.shapes[i]}. "
            else:
                description += f"{method.title()} the {self.shapes[prev]} is a {self.shapes[i]}. "
            prev = i

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


