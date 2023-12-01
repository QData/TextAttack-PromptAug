from promptaug import PromptAugmenter

class BackTranslationAugmenter(PromptAugmenter):
    """Sentence level augmentation that uses MarianMTModel to back-translate.

    https://huggingface.co/transformers/model_doc/marian.html
    """

    def __init__(self, **kwargs):
        from textattack.transformations.sentence_transformations import BackTranslation
        from textattack.constraints.semantics.sentence_encoders import BERT
        # constraints = [BERT()]
        constraints = []

        transformation = BackTranslation(chained_back_translation=5)
        super().__init__(transformation, constraints = [], **kwargs)