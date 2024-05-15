from pydantic import BaseModel

class TranslationInput(BaseModel):
    source: str
    target: str
    text: str


class TextInput(BaseModel):
    text: str