import json

from shapes import Shape

def json_to_shapes(filepath):
    with open(filepath, "r") as file:
        shapes = json.load(file)
        
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
                if shape2.left < shape1.left:
                    relations["Left"].append(j)
                if shape2.right > shape1.right:
                    relations["Right"].append(j)
                if shape2.top > shape1.top:
                    relations["Above"].append(j)
                if shape2.bottom < shape1.bottom:
                    relations["Below"].append(j)
        relationships.append(relations)

    # Sort all the relationships
    relations["Left"].sort(key=lambda i: shapes[i].center[0], reverse=True)
    relations["Right"].sort(key=lambda i: shapes[i].center[0])
    relations["Above"].sort(key=lambda i: shapes[i].center[1])
    relations["Below"].sort(key=lambda i: shapes[i].center[1], reverse=True)

    return relationships
