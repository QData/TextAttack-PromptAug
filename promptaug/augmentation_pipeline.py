class AugmentationPipeline:

    def __init__(self, augmenter, model):
        self.augmenter = augmenter
        self.model = model

    def run(self, prompts):
        results = []
        for prompt in prompts:
            print(self.augmenter)
            augmented_prompts = self.augmenter.augment(prompt)

            for augmented_prompt in augmented_prompts:
                response = self.model.generate(augmented_prompt)
                results.append((augmented_prompt, response))

        return results