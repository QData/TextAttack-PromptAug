from promptaug.models import ChatModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class FlanT5(ChatModel):

    def __init__(self, size="base"):
        size = size.lower()
        valid_sizes = {"small", "base", "large", "xl", "xxl"}
        assert size in valid_sizes, f"size must be one of {valid_sizes}"

        model_name = f"google/flan-t5-{size}"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
