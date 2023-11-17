import sys
import os
import random
import json

from datasets.utils import json_to_shapes, get_relationships


class DescriptionGenerator:

    def __init__(self, shapes):
        self.shapes = shapes
        self.relationships = get_relationships(shapes)


    @classmethod
    def from_file(cls, filename):
        return cls(json_to_shapes(filename))


    def generate_descriptions(self):
        name_to_function = {
            "full": self._full, 
            "partial": self._partial,
            "coordinates": self._coordinates,
        }

        results = {}
        for name, function in name_to_function.items():
            try:
                results[name] = function()
            except NotImplementedError:
                pass

        return results


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
                    direction = f"to the {y_dir.lower()} {x_dir.lower()} of"
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

        for i in range(0, len(self.shapes)):
            shape1 = self.shapes[i]
            description += f"There is a {shape1} in the canvas. "
            for j in range(i + 1, len(self.shapes)):
                x_dir, y_dir = self.get_direction(i, j)

                if x_dir and y_dir:
                    direction = f"to the {y_dir.lower()} {x_dir.lower()} of"
                elif x_dir:
                    direction = f"{x_dir.lower()} of"
                else:
                    direction = y_dir.lower()
                    
                description += f"A {self.shapes[j]} is {direction} this {shape1}. "

        return description


    def _short(self):
        """
        Describe the relative relationship of an object to exactly one other object
        For n objects, we get n - 1 relations

        """
        raise NotImplementedError


    def _coordinates(self):
        """
        Describe the coordinate position of every object

        """
        if len(self.shapes) == 1:
            description = f"There is {len(self.shapes)} shape in a canvas. "
        else:
            description = f"There are {len(self.shapes)} shapes in a canvas. "

        for shape in self.shapes:
            description += f"There is a {shape} at {(shape.center[0], shape.center[1])} "
            if shape.name == "Circle":
                description += f"with radius {shape.radius}. "
            else:
                description += f"with side length {shape.length}. "

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
        gen = DescriptionGenerator.from_file(f"data/canvas_{n_shapes}_{i}.json")
        descriptions = gen.generate_descriptions()

        with open(f"{DATA_ROOT}/canvas_{n_shapes}_{i}.json", "w") as file:
            json.dump(descriptions, file, indent=4)

