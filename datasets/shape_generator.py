import random
import json
import sys
import os

from itertools import product

from shapes import Circle, Square, Triangle
from constants import *


def generate(n_shapes, n_examples):
    constructors = {
        "Circle": Circle, 
        "Square": Square, 
        "Triangle": Triangle
    }
    valid_choices = list(product(SHAPES, COLORS, SIZES))
    if n_shapes > len(valid_choices):
        print("Warning: The number of shapes exceeds the number of possible shape combinations")

    for i in range(0, n_examples):
        shapes = []

        random.shuffle(valid_choices)

        for j in range(0, n_shapes):
            valid = False

            index = j % len(valid_choices)
            shape_type = valid_choices[index][0]
            color = valid_choices[index][1]
            size = valid_choices[index][2]
            while not valid:
                valid = True
                
                center = (
                    random.randint(X_MIN, X_MAX),
                    random.randint(Y_MIN, Y_MAX))
                candidate = constructors[shape_type](color, size, center)
                
                for shape in shapes:
                    if candidate.intersect(shape):
                        valid = False
                        break
                        
                if not candidate.inbounds():
                    valid = False
                        
            shapes.append(candidate)
                
        with open(f"{DATA_ROOT}/canvas_{n_shapes}_{i}.json", "w") as file:
            json.dump([shape.to_json() for shape in shapes], file, indent=4)


if __name__ == "__main__":
    SEED = 37
    DATA_ROOT = "data/canvases"

    random.seed(SEED)
    if len(sys.argv) != 3:
        print("Usage: python shape_generator.py <number of shapes in canvas> <number of example canvases>")
        exit()

    n_shapes, n_examples = map(int, sys.argv[1:])
    print(f"Generating {n_examples} examples with {n_shapes} shape(s).")

    if not os.path.isdir(DATA_ROOT):
        os.makedirs(DATA_ROOT)

    generate(n_shapes, n_examples)

