from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Prompt_structure(BaseModel):
    response: str
    emotion_classification: str
    risk_assessment: Literal["low", "moderate", "high"]
    should_continue: Literal["proceed", "deflect", "stop"]