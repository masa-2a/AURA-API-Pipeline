from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class AIResponse(BaseModel):
    """Structure for AI model responses with safety assessment"""
    response: str
    emotion_classification: str
    risk_assessment: Literal["low", "moderate", "high"]
    should_continue: Literal["proceed", "stop"]

# Keep old name for backwards compatibility
Prompt_structure = AIResponse