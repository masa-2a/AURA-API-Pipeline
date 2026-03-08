"""
Reddit Mental Health Dataset - Input Schema
============================================

This schema is designed for the Reddit mental health dataset.

JSON structure:
{
    "id": 0,
    "text": "He said he had not felt that way before...",
    "label": "mild"
}

Fields:
- id: Unique identifier
- text: The mental health related post/prompt
- label: Severity level (minimum, mild, moderate, severe)
"""

from pydantic import BaseModel, model_validator
from typing import Optional


class RedditPrompt(BaseModel):
    """
    Input schema for Reddit mental health dataset.
    
    This handles the Reddit dataset which has:
    - id (int)
    - text (str) - the actual post content
    - label (str) - severity classification (minimum/mild/moderate/severe)
    """
    
    # Fields from JSON
    id: int
    text: str
    label: Optional[str] = None  # Severity label from dataset
    
    # Compatibility fields (required by providers)
    prompt: Optional[str] = None  # What gets sent to AI
    category: Optional[str] = None  # Maps to label
    
    @model_validator(mode='before')
    @classmethod
    def setup_fields(cls, data):
        """
        Map Reddit dataset fields to provider-compatible fields.
        
        - text → prompt (what AI sees)
        - label → category (for output tracking)
        """
        if isinstance(data, dict):
            # Use text as the prompt
            data['prompt'] = data.get('text', '')
            
            # Map label to category
            if 'label' in data and 'category' not in data:
                data['category'] = data['label']
        
        return data
    
    def __repr__(self):
        return f"<RedditPrompt id={self.id} severity={self.label}>"
