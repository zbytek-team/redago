from transformers import pipeline, MT5Tokenizer, TFMT5ForConditionalGeneration
from redago_core.correctors.base_corrector import BaseCorrector
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
ORT_MODEL_NAME = os.getenv("MODEL_NAME")


class CommaCorrector(BaseCorrector):
    def __init__(self):
        tokenizer_test = MT5Tokenizer.from_pretrained("google/mt5-small", legacy=False)
        model_test = TFMT5ForConditionalGeneration.from_pretrained( ORT_MODEL_NAME, token=HUGGINGFACE_TOKEN)

        self._pipe = pipeline("text2text-generation", model=model_test, tokenizer=tokenizer_test)

    def correct(self, sentence: str) -> str:
        sentence = "<ort> " + sentence
        return self._pipe(sentence)[0]["generated_text"]
