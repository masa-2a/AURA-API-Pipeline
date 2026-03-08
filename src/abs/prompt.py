from pydantic import BaseModel, Field, model_validator
from typing import Optional

'''
Prompt class
'''
class Prompt(BaseModel):
    id: Optional[int] = None
    text: str
    category: Optional[str] = None
    prompt: Optional[str] = None
    
    @model_validator(mode='before')
    @classmethod
    def set_prompt(cls, data):
        """Auto-populate prompt field from text if not provided"""
        if isinstance(data, dict):
            if 'prompt' not in data or data['prompt'] is None:
                data['prompt'] = data.get('text', '')
            # Handle both 'label' and 'category' field names
            if 'label' in data and 'category' not in data:
                data['category'] = data['label']
        return data
    
    def __repr__(self):
        return f"<Prompt id={self.id} category={self.category}>"