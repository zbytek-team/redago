from dataclasses import dataclass
from litestar import Litestar, post
from redago_core.correctors.comma_corrector import CommaCorrector
from litestar.config.cors import CORSConfig
from pydantic import BaseModel

@dataclass
class TextCorrectionRequest:
    text: str

class TextResponse(BaseModel):
    text: str


comma_corrector = CommaCorrector()


@post("/correct")
async def correct_text(data: TextCorrectionRequest) -> TextResponse:
    corrected_text = comma_corrector.correct(data.text)
    return TextResponse(text=corrected_text)


cors_config = CORSConfig(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])    

app = Litestar([correct_text], cors_config=cors_config)