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
    risk_level: Optional[str] = "low"  # "low", "medium", "high"
    
    def __init__(self, text: str, category: str, id: int, risk_level: str = "low"):
        super().__init__(
            id=id,
            text=text,
            prompt = text,
            category=category,
            risk_level=risk_level
        )
    
    def __repr__(self):
        return f"<Prompt id={self.id} category={self.category} risk={self.risk_level}>"