from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
from pydantic import BaseModel, Field
from time import perf_counter

'''
GPT client adapter so aggregator doesnt have to worry about response structure
'''
class ProviderResult(BaseModel):
    provider: str
    text: str                              # normalized assistant text
    error: Optional[str] = None

class Provider(ABC):
    name: str

    @abstractmethod
    async def generate(self, prompt_text: str, **kwargs) -> ProviderResult:
        ...
