from abc import ABC

class Task(ABC):

    def __init__(self, prompts, dataset, modify_data=False):
        """
        An abstract class to represent a generic task. An element of a task 
        consists of two components, a prompt and a data sample. 

        """
        self.prompts = prompts
        self.dataset = dataset
        self.modify_data = modify_data

    # Task type
    # Task dataset
    # Prompts
    #   Make prompt a dataclass and make it provide its own labelconstraint
    #   Make dataset a class
    # Augment a prompt

    


