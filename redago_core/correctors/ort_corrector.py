from transformers import pipeline, MT5Tokenizer, TFMT5ForConditionalGeneration
from redago_core.correctors.base_corrector import BaseCorrector
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
ORT_MODEL_NAME = os.getenv("ORT_MODEL_NAME")


class OrtCorrector(BaseCorrector):
    def __init__(self):
        tokenizer_test = MT5Tokenizer.from_pretrained("google/mt5-small", legacy=False)
        model_test = TFMT5ForConditionalGeneration.from_pretrained( ORT_MODEL_NAME, token=HUGGINGFACE_TOKEN)

        self._pipe = pipeline("text2text-generation", model=model_test, tokenizer=tokenizer_test, max_length=512)

    def correct(self, text: str) -> str:
        text = "<ort> " + text
        return self._pipe(text)[0]["generated_text"]
