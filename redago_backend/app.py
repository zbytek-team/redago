from dataclasses import dataclass
from litestar import Litestar, post
from litestar.config.cors import CORSConfig
from pydantic import BaseModel

from redago_core.corrector import Corrector
from redago_core.correctors.comma_corrector import CommaCorrector
from redago_core.correctors.simple_corrector import SimpleCorrector


@dataclass
class TextCorrectionRequest:
    text: str

class TextResponse(BaseModel):
    text: str

class TokenizedTextResponse(BaseModel):
    tokenized_text: list


corrector = Corrector([CommaCorrector(), SimpleCorrector()])


@post("/correct")
async def correct_text(data: TextCorrectionRequest) -> TextResponse:
    corrected_text = corrector.correct(data.text)
    return TextResponse(text=corrected_text)

@post("/correct-tokenized")
async def correct_text_tokenized(data: TextCorrectionRequest) -> TokenizedTextResponse:
    corrected_text = corrector.correct(data.text)
    text = data.text

    tokenized_text = []

    for text_word, corrected_word in zip(text.split(), corrected_text.split()):
        reason = ["ok"]
        if text_word != corrected_word:
            reason.clear()
            if text_word.lower() == corrected_word.lower():
                reason.append("case")

            if corrected_word[-1] == "," and text_word[-1] != ",":
                reason.append("comma")
                if corrected_word[:-1].lower() != text_word.lower():
                    reason.append("ortography")
            
            if text_word[-1] == "," and corrected_word[-1] != ",":
                reason.append("nocomma")
                if corrected_word.lower() != text_word[:-1].lower():
                    reason.append("ortography")

            if corrected_word[-1] == "." and text_word[-1] != ".":
                reason.append("period")
                if corrected_word[:-1].lower() != text_word.lower():
                    reason.append("ortography")

            if corrected_word[-1] not in [".", ","] and text_word[-1] not in [".", ","] and corrected_word.lower() != text_word.lower():
                reason.append("ortography")
        
        tokenized_text.append({
            "text": text_word,
            "corrected": corrected_word,
            "reason": reason
        })

    return TokenizedTextResponse(tokenized_text=tokenized_text)


cors_config = CORSConfig(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])    

app = Litestar([correct_text, correct_text_tokenized], cors_config=cors_config)