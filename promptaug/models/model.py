import json
import os
import openai
import time 
import requests

from tenacity import retry, stop_after_attempt, wait_random_exponential


CACHE_DIR = "/p/qdatatext/ki4km/models"
LLAMA_WEIGHTS_DIR = f"{CACHE_DIR}/models--facebook--llama-7B"
ALPACA_WEIGHTS_DIR = f"{CACHE_DIR}/models--stanford--alpaca--7B"

class Model:

    def __init__(self, model_name, is_gpu):
        self.model_name = model_name
        self.is_gpu = is_gpu

        self._load_model()


    def _load_model(self):
        if self.model_name == "flan-t5":
            from transformers import T5Tokenizer, T5ForConditionalGeneration
            tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl", cache_dir=CACHE_DIR)
            model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto", cache_dir=CACHE_DIR)
        elif self.model_name == "gpt-j":
            from transformers import AutoModelForCausalLM, AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B", cache_dir=CACHE_DIR)
            model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", device_map="auto", cache_dir=CACHE_DIR)
        elif self.model_name == "dolly":
            from transformers import AutoModelForCausalLM, AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v1-6b", cache_dir=CACHE_DIR)
            model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v1-6b", device_map="auto", cache_dir=CACHE_DIR)
        elif self.model_name == "llama":
            from transformers import AutoTokenizer, LlamaForCausalLM
            tokenizer = AutoTokenizer.from_pretrained(LLAMA_WEIGHTS_DIR)
            model = LlamaForCausalLM.from_pretrained(LLAMA_WEIGHTS_DIR, device_map="auto")
        elif self.model_name == "alpaca":
            from transformers import AutoModelForCausalLM, AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(ALPACA_WEIGHTS_DIR)
            model = AutoModelForCausalLM.from_pretrained(ALPACA_WEIGHTS_DIR, device_map="auto")
        else:
            tokenizer = None
            model = None

        if self.model_name == "chat-gpt":
            openai.api_key = os.getenv("OPENAI_API_KEY")

        self.tokenizer = tokenizer
        self.model = model


    @retry(wait=wait_random_exponential(min=20, max=60), stop=stop_after_attempt(6))
    def gpt_api_call(self, input_string):
        time.sleep(5)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": input_string}
            ],
            top_p=0.9,
            max_tokens=50
        )
        return completion.choices[0].message["content"]


    @retry(wait=wait_random_exponential(min=3, max=20), stop=stop_after_attempt(6))
    def huggingface_api_call(self, api_url, input_string):
        HF_API_TOKEN = os.getenv("HF_API_KEY")
        parameters = {
            "max_new_tokens": 50,
            "top_p": 0.9,
            "do_sample": False,
            "early_stopping": False,
        }
        payload = {"inputs": input_string, "parameters": parameters,"options" : {"use_cache": False} }
        response = requests.request("POST", api_url, json=payload, headers={"Authorization": f"Bearer {HF_API_TOKEN}"})
        data = json.loads(response.content.decode("utf-8"))
        if "error" in data and "estimated_time" in data:
            time.sleep(data["estimated_time"])
        
        return data[0]["generated_text"]


    def flan_ul2_api_call(self, input_string):
        return self.huggingface_api_call("https://api-inference.huggingface.co/models/google/flan-ul2", input_string)


    def generate(self, input_string):
        if self.model_name == "chat-gpt":
            return self.gpt_api_call(input_string)
        if self.model_name == "flan-ul2":
            return self.flan_ul2_api_call(input_string)

        # Code for transformer models
        input_ids = self.tokenizer(input_string, return_tensors="pt").input_ids
        if self.is_gpu:
            input_ids = input_ids.to("cuda")

        outputs = self.model.generate(
            input_ids, 
            max_new_tokens=50,
            top_p=0.9,
            do_sample=False,
            early_stopping=False,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if self.model_name in {"gpt-j", "dolly", "alpaca", "llama"}:
            answer = answer[len(input_string):]
        return answer


