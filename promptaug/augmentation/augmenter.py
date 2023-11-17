from itertools import product
from textattack.augmentation import Augmenter

class PromptAugmenter:

    def __init__(
        self, 
        prompts,
        transformations,
        pct_words_to_swap=0.1,
        transformations_per_example=1,
        high_yield=False,
        fast_augment=False,
        enable_advanced_metrics=False
    ):
        assert len(prompts) == len(transformations), "there must be one transformation per prompt"

        self.prompts = prompts
        self.augmenters = []
        for prompt, transformation in zip(prompts, transformations):
            if prompt.modifiable:
                self.augmenters.append(Augmenter(
                    transformation,
                    prompt.constraints,
                    pct_words_to_swap,
                    transformations_per_example,
                    high_yield,
                    fast_augment,
                    enable_advanced_metrics
                ))
            else:
                self.augmenters.append(None)


    def augment(self):
        perturbed_texts = []

        for i, prompt in enumerate(self.prompts):
            if prompt.modifiable:
                perturbed_texts.append(self.augmenters[i].augment(prompt.text))
            else:
                perturbed_texts.append([prompt.text])

        return [" ".join(prompt) for prompt in product(*perturbed_texts)]

    

