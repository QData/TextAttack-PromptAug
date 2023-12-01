from textattack.shared import AttackedText

class AugmentationTemplate:

    def __init__(self, text, prompt_constraints=[None, None]):
        self.text = text
        self.prompt_constraints = prompt_constraints


    def get_prompt_pairs(self):
        return zip(self.prompt_constraints, self.text)