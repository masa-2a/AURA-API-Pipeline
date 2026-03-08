"""
Mental Health Safety Response Schema
=====================================

This schema is designed for mental health safety evaluation tasks.

The AI will return:
- response: The actual text response to the user
- emotion_classification: Detected emotion (anxiety, depression, neutral, etc.)
- risk_assessment: Safety level (low, moderate, high)
- should_continue: Whether AI should continue conversation or deflect (proceed, stop)

This matches the current AIResponse but is specific to mental health evaluation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MentalHealthResponse(BaseModel):
    """
    Output schema for mental health safety evaluation.
    
    Forces AI to provide:
    1. A supportive response
    2. Emotion classification
    3. Risk assessment
    4. Decision to continue or deflect
    """
    
    response: str = Field(
        description="The AI's supportive response to the user"
    )

    label: Literal["minimum", "mild", "moderate", "severe"] = Field(
        description="Safety risk level assessment"
    )
    
    should_continue: Literal["proceed", "stop"] = Field(
        description="Whether to continue conversation (proceed) or deflect to professional help (stop)"
    )
    
    emotion_classification: str = Field(
        description="Detected emotion (e.g., anxiety, depression, neutral, joy)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I understand you're going through a difficult time. It's important to talk to someone who can help.",
                "emotion_classification": "anxiety",
                "risk_assessment": "moderate",
                "should_continue": "stop"
            }
        }
