from transformers import AutoTokenizer, pipeline
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")


class CommaCorrector:
    def __init__(self):
        self._pipe = pipeline(
            "ner",
            MODEL_NAME,
            aggregation_strategy="none",
            use_auth_token=HUGGINGFACE_TOKEN
        )

    def process_sentence(self, sentence: str) -> list:
        return self._pipe(sentence)
    
    def get_positions(self, sentence: str) -> list:
        comma_positions = []
        comma_required = False
        skip_first_word = True
        last_word = None

        for word in self.process_sentence(sentence):
            if skip_first_word:
                skip_first_word = False
                last_word = word
                continue

            # Check if a comma should be inserted
            if last_word["entity"] == "LABEL_1" or comma_required:
                comma_required = True
                if word["start"] == last_word["end"]:
                    comma_positions.append(word["start"])
                else:
                    comma_positions.append(last_word["end"])
                    comma_required = False

            last_word = word

        return comma_positions

    def correct(self, sentence: str) -> str:
        comma_positions = self.get_positions(sentence)
        sentence = list(sentence)

        for position in comma_positions:
            sentence.insert(position, ",")

        return "".join(sentence)
