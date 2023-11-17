from textattack.constraints import PreTransformationConstraint

class PromptConstraint(PreTransformationConstraint):
    
    # This could be words or specific indices
    # Rename this to WordConstraint?
    def __init__(self, unmodifiable_words):
        self.unmodifiable_words = {word.lower() for word in unmodifiable_words}

    def _get_modifiable_indices(self, current_text):
        modifiable_indices = set()
        for i, word in enumerate(current_text.words):
            if word.lower() not in self.unmodifiable_words:
                modifiable_indices.add(i)
        return modifiable_indices

    def check_compatibility(self, transformation):
        return True


