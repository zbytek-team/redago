from transformers import pipeline, AutoTokenizer
from redago_core.correctors.base_corrector import BaseCorrector
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

class CommaCorrector(BaseCorrector):
    def __init__(self):
        self._pipe = pipeline(
            "ner",
            MODEL_NAME,
            aggregation_strategy="none",
            token=HUGGINGFACE_TOKEN
        )
        self._tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME, token=HUGGINGFACE_TOKEN
        )

    def correct(self, sentence: str) -> str:
        sentence = sentence.replace(",", " ")
        sentence = sentence.strip()
        sentence = self._pipe(sentence)

        comma_required = False
        corrected_sentence = []
        skip_first_word = True
        last_word = None

        for word in sentence:
            if skip_first_word:
                skip_first_word = False
                last_word = word
                corrected_sentence.append(word["word"])
                continue

            # Check if a comma should be inserted
            if last_word["entity"] == "LABEL_1" or comma_required:
                comma_required = True
                if word["start"] == last_word["end"]:
                    corrected_sentence.append(word["word"])
                else:
                    corrected_sentence.append(",")
                    corrected_sentence.append(word["word"])
                    comma_required = False
            else:
                corrected_sentence.append(word["word"])

            last_word = word

        return self._tokenizer.convert_tokens_to_string(corrected_sentence)
