import torch
import wikipedia as wp
from transformers import BertTokenizer, BertForQuestionAnswering
from typing import List, Tuple


class BERTLLMClient:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

    def ask(self, question: str) -> str:
        # Use wikipedia library to search for a summary of the topic
        first_result: str = wp.search(question)[0]
        page: wp.WikipediaPage = wp.page(first_result, auto_suggest=False)
        text: str = page.content

        # Provide context from the Wikipedia page to BERT
        inputs: dict = self.tokenizer.encode_plus(question,
                                                  text,
                                                  add_special_tokens=True,
                                                  return_tensors='pt',
                                                  truncation=True)
        input_ids: List[int] = inputs["input_ids"].tolist()[0]

        # Get the model's predictions for the start and end positions of the answer
        outputs: Tuple[torch.Tensor, ...] = self.model(**inputs)
        answer_start_scores: torch.Tensor = outputs.start_logits
        answer_end_scores: torch.Tensor = outputs.end_logits

        # Extract the answer
        answer_start: int = torch.argmax(answer_start_scores)
        answer_end: int = torch.argmax(answer_end_scores) + 1
        answer: str = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

        return answer
