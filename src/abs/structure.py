from pydantic import BaseModel, Field
from typing import List, Optional

class Prompt_structure(BaseModel):
    response: str
    emotion_classification: str