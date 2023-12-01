from itertools import product

from textattack.augmentation import Augmenter
from promptaug.constraints import PromptConstraint, UnmodifiableConstraint

class PromptAugmenter:

    def __init__(
        self, 
        transformation,
        constraints=[],
        pct_words_to_swap=0.1,
        transformations_per_example=1,
        high_yield=False,
        fast_augment=False,
        enable_advanced_metrics=False
    ):
        self.augmenter = Augmenter(
            transformation,
            constraints,
            pct_words_to_swap,
            transformations_per_example,
            high_yield,
            fast_augment,
            enable_advanced_metrics
        )


    def augment(self, augmentable_prompt):
        perturbed_texts = []

        for prompt_constraint, prompt in augmentable_prompt.get_prompt_pairs():
            if not isinstance(prompt_constraint, UnmodifiableConstraint):
                if prompt_constraint is not None:
                    self.augmenter.pre_transformation_constraints.append(prompt_constraint)

                print()
                print(self.augmenter)
                print()

                augmented_prompts = self.augmenter.augment(prompt)
                if prompt_constraint is not None:
                    self.augmenter.pre_transformation_constraints.pop()
            else:
                augmented_prompts = [prompt] * self.augmenter.transformations_per_example

            if len(perturbed_texts) == 0:
                perturbed_texts = augmented_prompts
            else:
                for i in range(0, len(perturbed_texts)):
                    perturbed_texts[i] += " " + augmented_prompts[i]
                

        return perturbed_texts

    

