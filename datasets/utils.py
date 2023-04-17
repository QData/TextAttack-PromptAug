import json

from datasets.shapes import Shape

def json_to_shapes(filepath):
    with open(filepath, "r") as file:
        shapes = json.load(file)["canvas"]
        
    result = []
    for shape in shapes:
        constructor = Shape.get_constructor(shape["shape"])
        result.append(constructor(shape["color"], shape["size"], shape["center"]))
        
    return result


def get_relationships(shapes):
    relationships = []
    for i, shape1 in enumerate(shapes):
        relations = {
            "Left": [],
            "Right": [],
            "Above": [],
            "Below": []
        }
        
        for j, shape2 in enumerate(shapes):
            if i != j:
                # Pay attention to the case where a larger object "swallows" a smaller one
                if not (shape2.left < shape1.left and shape2.right > shape1.right):
                    if shape2.left < shape1.left:
                        relations["Left"].append(j)
                    if shape2.right > shape1.right:
                        relations["Right"].append(j)

                if not (shape2.top > shape1.top and shape2.bottom < shape1.bottom):
                    if shape2.top > shape1.top:
                        relations["Above"].append(j)
                    if shape2.bottom < shape1.bottom:
                        relations["Below"].append(j)

        # Sort all the relationships
        relations["Left"].sort(key=lambda i: shapes[i].left, reverse=True)
        relations["Right"].sort(key=lambda i: shapes[i].right)
        relations["Above"].sort(key=lambda i: shapes[i].top)
        relations["Below"].sort(key=lambda i: shapes[i].bottom, reverse=True)

        relationships.append(relations)

    return relationships
