
from pydantic import BaseModel, Field
from typing import Optional

'''
Prompt class
'''
class Prompt(BaseModel):
    id: Optional[int] = None
    text: str
    category: Optional[str] = None

    def __repr__(self):
        return f"<Prompt id={self.id} category={self.category}>"