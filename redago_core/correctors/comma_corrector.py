from transformers import pipeline, AutoTokenizer
from redago_core.correctors.base_corrector import BaseCorrector
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")


class CommaCorrector(BaseCorrector):
    def __init__(self):
        self._pipe = pipeline(
            "ner", MODEL_NAME, aggregation_strategy="none", token=HUGGINGFACE_TOKEN
        )
        self._tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME, token=HUGGINGFACE_TOKEN
        )

    def correct(self, text: str) -> str:
        text = text.replace(",", " ")
        text = text.strip()
        text = self._pipe(text)

        comma_required = False
        corrected_text = []
        skip_first_word = True
        last_word = None

        for word in text:
            if skip_first_word:
                skip_first_word = False
                last_word = word
                corrected_text.append(word["word"])
                continue

            # Check if a comma should be inserted
            if last_word["entity"] == "LABEL_1" or comma_required:
                comma_required = True
                if word["start"] == last_word["end"]:
                    corrected_text.append(word["word"])
                else:
                    corrected_text.append(",")
                    corrected_text.append(word["word"])
                    comma_required = False
            else:
                corrected_text.append(word["word"])

            last_word = word

        return self._tokenizer.convert_tokens_to_string(corrected_text)
