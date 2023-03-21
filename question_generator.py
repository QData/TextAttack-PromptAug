import json
import random

from datasets.shapes import Circle, Square, Triangle
from datasets.constants import SHAPES, SIZES, COLORS

def json_to_shapes(filepath):
    constructors = {
        "Circle": Circle, 
        "Square": Square, 
        "Triangle": Triangle
    }
    shapes = None
    with open(filepath, "r") as file:
        shapes = json.load(file)
        
    result = []
    for shape in shapes:
        constructor = constructors[shape["shape"]]
        result.append(constructor(shape["color"], shape["size"], shape["center"]))
        
    return result


class QuestionGenerator:
    
    def __init__(self, shapes):
        self.shapes = shapes
        self.relationships = []
        
        for i, shape1 in enumerate(shapes):
            relations = {
                "Left": [],
                "Right": [],
                "Above": [],
                "Below": []
            }
            
            for j, shape2 in enumerate(shapes):
                if i != j:
                        if shape2.left < shape1.left:
                            relations["Left"].append(j)
                        if shape2.right > shape1.right:
                            relations["Right"].append(j)
                        if shape2.top > shape1.top:
                            relations["Above"].append(j)
                        if shape2.bottom < shape1.bottom:
                            relations["Below"].append(j)
            self.relationships.append(relations)
        
    @classmethod
    def from_file(cls, filename):
        return cls(json_to_shapes(filename))
    
    
    def existence(self, shape_value=None, color_value=None, size_value=None):
        for shape in self.shapes:
            if shape_value is None or shape.name == shape_value:
                if color_value is None or shape.color == color_value:
                    if size_value is None or shape.size == size_value:
                        return True
        return False
    
    
    def _shape_to_description(self, shape):
        return f"{shape.size.lower()} {shape.color.lower()} {shape.name.lower()}"


    def generate_short_description(self):
        if len(self.shapes) == 1:
            return f"There is a canvas with a {self._shape_to_description(self.shapes[0])}. "
        raise NotImplementedError
    
    
    def generate_full_description(self):
        description = f"There are {len(self.shapes)} shapes in a canvas. "
        
        for i, shape in enumerate(self.shapes):
            description += f"There is a {self._shape_to_description(shape)} in the canvas. "
            
            for direction, relation_indexes in self.relationships[i].items():
                for j in relation_indexes:
                    if direction in {"Left", "Right"}:
                        direction = f"to the {direction.lower()} of"
                    else:
                        direction = direction.lower()
                    
                    description += f"A {self._shape_to_description(self.shapes[j])} is {direction} this {self._shape_to_description(shape)}. "
        return description


    def generate_transitivity_promopt(self, horizontal=True):
        """
        Simple transitivity prompt for 3 objects

        """
        if len(self.shapes) != 3:
            raise NotImplementedError

        description = "There are 3 shapes in a canvas. "
        if horizontal:
            i = random.randint(0, len(self.shapes) - 1)
            start = self.shapes[i]

            description += f"A {self._shape_to_description(start)} is in the canvas. "
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
                direction1 = "ERROR"
                direction2 = "ERROR"
                first = "ERROR"
                second = "ERROR"
                left = "ERROR"
                right = "ERROR"
                

            description += f"{direction1} of the {self._shape_to_description(start)} is a {self._shape_to_description(first)}. "
            description += f"{direction2} of the {self._shape_to_description(start)} is a {self._shape_to_description(second)}. "

            description += "\nQuestion: "
            if random.random() < 0.5:
                description += f"Where is the {self._shape_to_description(left)} relative to the {self._shape_to_description(right)}? "
                answer = "Left"
            else:
                description += f"Where is the {self._shape_to_description(right)} relative to the {self._shape_to_description(left)}? "
                answer = "Right"

        else:
            pass


        return description, answer
        
    def generate_existence_questions(self):
        qa = []
        
        # Single Attribute
        for shape_type in SHAPES:
            qa.append((
                f"Is there a {shape_type.lower()}?", 
                "Yes" if self.existence(shape_value=shape_type) else "No"
            ))
        for color in COLORS:
            qa.append((
                f"Is there a shape that is {color.lower()}?", 
                "Yes" if self.existence(color_value=color) else "No"
            ))
        for size in SIZES:
            qa.append((
                f"Is there a {size.lower()} shape?",
                "Yes" if self.existence(size_value=size) else "No"
            ))

        # Double Attribute
        for shape_type in SHAPES:
            for color in COLORS:
                qa.append((
                    f"Is there a {color.lower()} {shape_type.lower()}?", 
                    "Yes" if self.existence(shape_value=shape_type, color_value=color) else "No"
                ))
            for size in SIZES:
                qa.append((
                    f"Is there a {size.lower()} {shape_type.lower()}?", 
                    "Yes" if self.existence(shape_value=shape_type, size_value=size) else "No"
                ))
        for color in COLORS:
            for size in SIZES:
                qa.append((
                    f"Is there a {size.lower()} {color.lower()} shape?",
                    "Yes" if self.existence(color_value=color, size_value=size) else "No"
                ))

        # Triple Attribute
        for shape_type in SHAPES:
            for color in COLORS:
                for size in SIZES:
                    qa.append((
                        f"Is there a {size.lower()} {color.lower()} {shape_type.lower()}?", 
                        "Yes" if self.existence(shape_value=shape_type, color_value=color, size_value=size) else "No"
                    ))
            
        return qa
