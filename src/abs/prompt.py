from pydantic import BaseModel, Field
from typing import Optional

'''
Prompt class
'''
class Prompt(BaseModel):
    id: Optional[int] = None
    text: str
    category: Optional[str] = None

    def __init__(self, text: str, category: str, id: int):
        self.id = id
        self.text = f"Respond to the following with a JSON object containing two keys: response_text and emotion_analysis: {text}"
        self.category = category

    def __repr__(self):
        return f"<Prompt id={self.id} category={self.category}>"