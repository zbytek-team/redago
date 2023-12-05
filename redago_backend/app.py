from dataclasses import dataclass
from litestar import Litestar, post, get
from litestar.config.cors import CORSConfig
from pydantic import BaseModel

from redago_core.corrector import Corrector
from redago_core.correctors.comma_corrector import CommaCorrector
from redago_core.correctors.simple_corrector import SimpleCorrector
from redago_core.correctors.ort_corrector import OrtCorrector
from redago_backend import utils


@dataclass
class TextCorrectionRequest:
    text: str


class TextResponse(BaseModel):
    text: str


class TokenizedTextResponse(BaseModel):
    tokenized_text: list


corrector = Corrector([SimpleCorrector(), OrtCorrector(), CommaCorrector()])


@get("/")
async def index() -> TextResponse:
    return TextResponse(text="Redago backend")


@post("/correct")
async def correct_text(data: TextCorrectionRequest) -> TextResponse:
    corrected_text = corrector.correct(data.text)
    return TextResponse(text=corrected_text)


@post("/correct-with-reason")
async def correct_text_tokenized(data: TextCorrectionRequest) -> TokenizedTextResponse:
    corrected_text = corrector.correct(data.text)
    text = data.text

    tokenized_text = []

    for text_word, corrected_word in zip(text.split(), corrected_text.split()):
        reason = ["ok"]

        if not utils.checkIfWordsAreEqual(text_word, corrected_word):
            reason.clear()

            if utils.checkIfCaseChanged(text_word, corrected_word):
                reason.append("case_changed")

            if utils.checkIfCommaInserted(text_word, corrected_word):
                reason.append("comma_inserted")

            if utils.checkIfCommaRemoved(text_word, corrected_word):
                reason.append("comma_removed")

            if utils.checkIfPeriodInserted(text_word, corrected_word):
                reason.append("period_inserted")

            if utils.checkIfPeriodRemoved(text_word, corrected_word):
                reason.append("period_removed")

            if utils.checkIfSpellingChanged(text_word, corrected_word):
                reason.append("spelling_changed")

        tokenized_text.append(
            {"text": text_word, "corrected": corrected_word, "reason": reason}
        )

    return TokenizedTextResponse(tokenized_text=tokenized_text)


cors_config = CORSConfig(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app = Litestar([correct_text, correct_text_tokenized], cors_config=cors_config)
