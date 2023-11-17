from textattack.shared import AttackedText

class Prompt:

    def __init__(self, text_input, constraints=[], modifiable=True):
        self.text = text_input  # Or should this be attacked text?
        self.constraints = constraints 
        self.modifiable = modifiable
    
    