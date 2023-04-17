# Tasks


### Adding a Task
To add a new task `NewTask`, create a file `new_task.py` and define the `NewTask` class, ensuring that it extends the `Task` baseclass. Each task must define the `generate_questions` method and may optionally override the `score` and `select_expected_answer` methods:

1. `generate_questions`: Given a list of shapes in the canvas, return a list of (question, answer) pairs for the task. The first pair in the list is used as the eveluation question for the model. The remaining pairs are used in the few-shot setting. Currently, all tasks return a list of length 3. This method also optionally takes a parameter `selected_answer`. If this is not none, the answer to the first question in the list should be `selected_answer`. 


2. `score` (optional): Given a file that contains the expected and actual answers, return score the model's answer. This score should be between 0 and 1, where 1 is a perfect answer and 0 is completly incorrect. The default `score` method assigns a score of 1 if the expected answer is contained in the actual answer. 

3. `select_expected_answer` (optional): Given the $i$ th item  of of $n$ data items being generated, return the desired expected answer for the evaluation question. This method aids in creating a balanced dataset. See `ExistenceTask` for an example. The default method returns `None` to have a completly random distribution. 


Once you have defined your new task, register it in `registered_tasks.py`. Depending on your task, there are potentially two additional steps:

1. If your task and its description are closely coupled, the task can create the description in cojuntion with the question-answer pairs. In this case, have your task set `self.description` during each call to `generate_questions`. See `TransitivityTask` for an example. 

2. Your task may add additional information to a description. In this case, you must have your task set `self.description` during each call to `generate_questions` AND you must modify `loader.py` to add this information to the description when the data is loaded. See `ExistenceTrackingTask` and `loader.py` for an example. 