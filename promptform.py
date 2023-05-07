"""
This file store the different forms of prompts.
""" 
def obstacles_string(obstacles):
    ob_promp = ''
    for pair in obstacles:
        ob_promp += '{},{} '.format(pair[0], pair[1])
    return ob_promp



def prompt1(start, end, size, obstacles):
    if obstacles == []:
        s = f"I'm in a maze that looks like a grid with 4 rows and 4 columns. " \
            f"I start at space (2,0). My goal is to reach the space (3, 3) in the maze."\
            f"To move through the maze, I can only move up, down, right or left. I can move only one space at a time, " \
            f"either directly up, down, up, or left, but not diagonally or in any other direction. " \
            f"Can you help me figure out the best way to navigate this maze from the start space to the ending space? " \
            f"Solution: " \
            f"Start at space (2,0). " \
            f"Move up to space (2,1). " \
            f"Move up to space (2,2). " \
            f"Move up to space (2,3). " \
            f"Move right to space (3,3). "\
            f"I'm in a maze that looks like a grid with {size} rows and {size} columns, " \
            f"I start at space {start[0]},{start[1]}. My goal is to reach the space {end[0]}, {end[1]} in the maze. " \
            f"To move through the maze, I can only move up, down, right or left. I can move one space at a time, " \
            f"either directly up or directly to the right, but not diagonally or in any other direction. " \
            f"Can you help me figure out the best way to navigate this maze from the start space to the ending space? " \
            f"Solution:"
    else:
        s = f"I'm in a maze that looks like a grid with 4 rows and 4 columns. " \
            f"I start at space 2,0. My goal is to reach the space 3, 3 in the maze."\
            f"There are some obstacles at place 3,1 and 3,0, in the maze,"\
            f"and I cannot go through those obstacles." \
            f"To move through the maze, I can only move up, down, right or left. I can move only one space at a time, " \
            f"either directly up, down, up, or left, but not diagonally or in any other direction. " \
            f"Can you help me figure out the best way to navigate this maze from the start space to the ending space? " \
            f"Solution: " \
            f"Start at space 2,0. " \
            f"Move up to space 2,1. " \
            f"Move up to space 2,2. " \
            f"Move up to space 2,3. " \
            f"Move right to space 3,3. "\
            f"I'm in a maze that looks like a grid with {size} rows and {size} columns, " \
            f"I start at space {start[0]},{start[1]}. My goal is to reach the space {end[0]}, {end[1]} in the maze. " \
            f"There are some obstacles at place" + obstacles_string(obstacles) + "in the maze,"\
            f"and I cannot go through those obstacles." \
            f"To move through the maze, I can only move up, down, right or left. I can move one space at a time, " \
            f"either directly up or directly to the right, but not diagonally or in any other direction. " \
            f"Can you help me figure out the best way to navigate this maze from the start space to the ending space? " \
            f"Solution:"

    return s


def prompt2(start, end, size, obstacles):
    if obstacles == []:
        s = f"I'm currently in a maze that looks like a grid with 4 rows and 4 columns.\
            I started from space 2,0 and my objective is to reach the space 3,3. However,\
            there are obstacles at locations 3,1 and 3,0 that I cannot pass through. To\
            navigate through the maze, I'm only allowed to move up, down, right, or left,\
            one space at a time. I cannot move diagonally or in any other direction. Can you\
            help me find the best way to reach my goal?\
            Here's the solution to the maze:\
            Start at space 2,0. \
            Move up to space 2,1. \
            Move up to space 2,2. \
            Move up to space 2,3. \
            Move right to space 3,3. \
            I'm currently in a maze that looks like a grid with {size} rows and {size} columns.\
            I started from space {start[0]},{start[1]} and my objective is to reach the space {end[0]}, {end[1]}. To\
            navigate through the maze, I'm only allowed to move up, down, right, or left,\
            one space at a time. I cannot move diagonally or in any other direction. Can you\
            help me find the best way to reach my goal?\
            Here's the solution to the maze:"           
        

    else:
        s = f"I'm currently in a maze that looks like a grid with 4 rows and 4 columns.\
            I started from space 2,0 and my objective is to reach the space 3,3. However,\
            there are obstacles at locations 3,1 and 3,0 that I cannot pass through. To\
            navigate through the maze, I'm only allowed to move up, down, right, or left,\
            one space at a time. I cannot move diagonally or in any other direction. Can you\
            help me find the best way to reach my goal?\
            Here's the solution to the maze:\
            Start at space 2,0. \
            Move up to space 2,1. \
            Move up to space 2,2. \
            Move up to space 2,3. \
            Move right to space 3,3. \
            I'm currently in a maze that looks like a grid with {size} rows and {size} columns.\
            I started from space {start[0]},{start[1]} and my objective is to reach the space {end[0]}, {end[1]}. However,\
            there are obstacles at locations" + obstacles_string(obstacles) + "that I cannot pass through. To\
            navigate through the maze, I'm only allowed to move up, down, right, or left,\
            one space at a time. I cannot move diagonally or in any other direction. Can you\
            help me find the best way to reach my goal?\
            Here's the solution to the maze:"