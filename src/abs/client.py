from abc import ABC, abstractmethod
from typing import List, Any
from src.abs.prompt import Prompt

class api_client(ABC):
    model_name: str

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @abstractmethod
    async def call(self, prompt: Prompt, **kwargs):
        """Send a single prompt to the API"""
        raise NotImplementedError

    async def batch_call(self, prompts: List[Prompt], **kwargs):
        """Optional method to batch multiple prompts"""
        pass

    async def retry_call(self, prompt: Prompt, max_retries: int, **kwargs):
        raise NotImplementedError

    def estimate_tokens(self, prompt: Prompt, response: Any) -> int:
        raise NotImplementedError
