from pydantic import BaseModel


class Sentences(BaseModel):
    text: str
