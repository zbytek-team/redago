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


corrector = Corrector([CommaCorrector(), SimpleCorrector()])


@post("/correct")
async def correct_text(data: TextCorrectionRequest) -> TextResponse:
    corrected_text = corrector.correct(data.text)
    return TextResponse(text=corrected_text)


cors_config = CORSConfig(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])    

app = Litestar([correct_text], cors_config=cors_config)