# Tasks


### Adding a Task
To add a new task `NewTask`, create a file `new_task.py` and define the `NewTask` class, ensuring that it extends the `Task` baseclass. Each task must define the `generate_questions` method and may optionally override the `score` and `select_expected_answer` methods:

1. `generate_questions`: Given a list of shapes in the canvas, return a list of (question, answer) pairs for the task. The first pair in the list is used as the eveluation question for the model. The remaining pairs are used in the few-shot setting. Currently, all tasks return a list of length 3. This method also optionally takes a parameter `selected_answer`. If this is not none, the answer to the first question in the list should be `selected_answer`. 


2. `score` (optional): Given a file that contains the expected and actual answers, return score the model's answer. This score should be between 0 and 1, where 1 is a perfect answer and 0 is completly incorrect. The default `score` method assigns a score of 1 if the expected answer is contained in the actual answer. 

3. `select_expected_answer` (optional): Given the $i$ th item  of of $n$ data items being generated, return the desired expected answer for the evaluation question. This method aids in creating a balanced dataset. See `ExistenceTask` for an example. The default method returns `None` to have a completly random distribution. 


Once you have defined your new task, register it in `registered_tasks.py`. Depending on your task, there are potentially two additional steps:

1. If your task and its description are closely coupled, the task can create the description in conjunction with the question-answer pairs. In this case, have your task set `self.description` during each call to `generate_questions`. Additionally, you must add the description name to `DESCRIPTION_TYPES` in `datasets/constants.py`. See `TransitivityTask` for an example. 

2. Your task may add additional information to a description. In this case, you must have your task set `self.description` during each call to `generate_questions` AND you must modify `loader.py` to add this information to the description when the data is loaded. See `ExistenceTrackingTask` and `loader.py` for an example. 

### Current Tasks

#### Existence Task
This task presents the description of the canvas to the model and asks if a certain object exists. For example, 
> There are 3 shapes in a canvas. There is a large red circle in the canvas. A small green circle is right of this large red circle. A small blue circle is to the above right of this large red circle. There is a small green circle in the canvas. A small blue circle is to the above left of this small green circle. There is a small blue circle in the canvas.  
Question: Is there a shape that is red?  
Expected answer is "Yes"


#### Count Task
This task presents the description of the canvas to the model and asks how many objects of a certain type exist. For example, 
> There are 3 shapes in a canvas. There is a large red triangle in the canvas. A large green circle is to the below right of this large red triangle. A small green square is to the below right of this large red triangle. There is a large green circle in the canvas. A small green square is to the above right of this large green circle. There is a small green square in the canvas.  
Question: How many large green triangles are there?  
Expected answer is "0"


#### Transitivity Task
This task presents the description of the canvas by choosing a shape as the "pivot point." Valid "pivot points" have at least one object to both their left and right OR at least one object both above and below them. The description of the canvas is the canvas is the shape that is the "pivot point" then all shapes in one direction and then all shapes in the other direction. The model is then asked for the relative position of two shapes that are not directly not to each other. For example, 
> There are 3 shapes in a canvas. There is a small blue square in the canvas. Below the small blue square is a small blue triangle. Above the small blue square is a large yellow circle.   
Question: Where is the small blue triangle relative to the large yellow circle?  
Expected answer is "Below"


#### Coordinate Task
This task presents the description of the canvas by giving the coordinate location of the center of each shape. The model is asked for the relative position of two shapes. For example, 
> There are 3 shapes in a canvas. There is a small red square at (16, 17). There is a large green triangle at (25, 15). There is a large blue triangle at (-6, 1).   
Question: Where is the large green triangle relative to the small red square?   
Expected answer is "Below Right"


#### Existence Tracking Task
This task presents the description of the canvas. Then shapes in the canvas are added and removed. The model is asked if a certain shape exists in the canvas after the additions and removals. For example, 
> There are 3 shapes in a canvas. There is a small blue circle in the canvas. A small red triangle is to the above left of this small blue circle. A large green circle is to the above left of this small blue circle. There is a small red triangle in the canvas. A large green circle is to the above left of this small red triangle. There is a large green circle in the canvas. A large blue triangle is added to the canvas. The large green circle is removed from the canvas. A small green triangle is added to the canvas.  
Question: Is there a large green circle in the canvas?  
Expected answer is "No"


#### Shuffle Tracking Task
This tasks presents the description of the canvas by descibing the order of the shapes in a line. Then the position of shapes in the canvas ae swapped. The model is asked what shape is at a certain position. For example, 
> There are 3 shapes in a canvas. From bottom to top, the shapes are a small blue triangle, a large blue square, and a large blue triangle. The large blue square and the large blue triangle swap positions. The small blue triangle and the large blue triangle swap positions. The large blue square and the small blue triangle swap positions.   
Question: What shape is second from the top?   
Expected answer is "Large Blue Square"

