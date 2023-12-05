from transformers import pipeline, MT5Tokenizer, TFMT5ForConditionalGeneration
from redago_core.correctors.base_corrector import BaseCorrector
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
ORT_MODEL_NAME = os.getenv("ORT_MODEL_NAME")


class OrtCorrector(BaseCorrector):
    def __init__(self):
        self.tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small", legacy=False)
        self.model = TFMT5ForConditionalGeneration.from_pretrained(ORT_MODEL_NAME, token=HUGGINGFACE_TOKEN)

    def correct(self, text: str) -> str:
        # split sentence by .
        sentences = text.split(".")
        # add <ort> to each sentence
        if text[-1] == ".":
            sentences = ["<ort> " + s + "." for s in sentences[:-1]]
        else:
            sentences = ["<ort> " + s for s in sentences]

        # encode sentences
        encoded = self.tokenizer(sentences, return_tensors="tf", padding=True)

        # generate
        outputs = self.model.generate(
            input_ids=encoded["input_ids"],
            attention_mask=encoded["attention_mask"],
            max_length=500
        )

        # decode
        decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

        return " ".join(decoded)
