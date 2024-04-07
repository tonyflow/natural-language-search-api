import os

from openai import OpenAI

import transformers, torch
import requests
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig


class LLaMAClient:
    # def __init__(self):
    #     self.tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf")
    #     self.model = LlamaForCausalLM.from_pretrained(
    #         pretrained_model_name_or_path="decapoda-research/llama-7b-hf",
    #         load_in_8bit=False,
    #         torch_dtype=torch.float16,
    #         device_map="auto",
    #     )

    def chat(self, message: str) -> str:
        # instruction = "How old is the universe?"
        # inputs = self.tokenizer(
        #     f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.
        # ### Instruction: {instruction}
        # ### Response:""",
        #     return_tensors="pt",
        # )
        # input_ids = inputs["input_ids"].to("cuda")
        #
        # generation_config = transformers.GenerationConfig(
        #     do_sample=True,
        #     temperature=0.1,
        #     top_p=0.75,
        #     top_k=80,
        #     repetition_penalty=1.5,
        #     max_new_tokens=128,
        # )
        #
        # with torch.no_grad():
        #     generation_output = self.model.generate(
        #         input_ids=input_ids,
        #         attention_mask=torch.ones_like(input_ids),
        #         generation_config=generation_config,
        #     )
        # output_text = self.tokenizer.decode(
        #     generation_output[0].cuda(), skip_special_tokens=True
        # ).strip()
        # print(output_text)
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
        headers = {"Authorization": "Bearer "}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs": "What is the most famous student of Plato?",
        })
        print(output)
        return "output"


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            organization='org-1QQNPDSxnOP3cc37drVi1UUA',
        )
        self.messages = []
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def chat(self, message: str) -> str:
        self.messages.append({
            "role": "user",
            "content": message
        })
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=50
        )
        # response = ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=self.messages,
        #     temperature=0,
        #     max_tokens=1000,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0
        # )

        response_message = response["choices"][0]["message"]
        self.messages.append(response_message)

        return response_message['content']
