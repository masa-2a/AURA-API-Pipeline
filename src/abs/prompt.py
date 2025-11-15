from pydantic import BaseModel, Field
from typing import Optional

'''
Prompt class
'''
class Prompt(BaseModel):
    id: Optional[int] = None
    text: str
    category: Optional[str] = None
    prompt: str
    
    def __init__(self, text: str, category: str, id: int):
        super().__init__(
            id=id,
            # text=f"Respond to the following with a JSON object containing two keys: response_text and emotion_analysis: {text}",
            text=text,
            prompt = text,
            category=category
        )
    
    def __repr__(self):
        return f"<Prompt id={self.id} category={self.category}>"