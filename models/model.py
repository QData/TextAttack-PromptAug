import os
import openai

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration

CACHE_DIR = "/p/qdatatext/ki4km/models/"

class Model:

    def __init__(self, model_name, is_gpu):
        self.model_name = model_name
        self.is_gpu = is_gpu

        self._load_model()


    def _load_model(self):
        if self.model_name == "flan-ul2":
            tokenizer = T5Tokenizer.from_pretrained("google/flan-ul2", cache_dir=CACHE_DIR)
            model = T5ForConditionalGeneration.from_pretrained("google/flan-ul2", device_map="auto", cache_dir=CACHE_DIR, torch_dtype=torch.bfloat16)
        elif self.model_name == "flan-t5":
            tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl", cache_dir=CACHE_DIR)
            model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto", cache_dir=CACHE_DIR)
        elif self.model_name == "gpt-j":
            tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B", cache_dir=CACHE_DIR)
            model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", device_map="auto", cache_dir=CACHE_DIR)
        else:
            tokenizer = None
            model = None

        if self.model_name == "chat-gpt":
            openai.api_key = os.getenv("OPENAI_API_KEY")

        self.tokenizer = tokenizer
        self.model = model


    def generate(self, input_string):
        if self.model_name == "chat-gpt":
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": input_string}
                ]
            )
            return completion.choices[0].message["content"]


        # Code for transformer models
        input_ids = self.tokenizer(input_string, return_tensors="pt").input_ids
        if self.is_gpu:
            input_ids = input_ids.to("cuda")

        outputs = self.model.generate(
            input_ids, 
            max_new_tokens=10,
            top_p=0.9,
            do_sample=False,
            early_stopping=False,
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if self.model_name == "gpt-j":
            answer = answer[len(input_string):]
        return answer


