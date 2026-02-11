from src.abs.client import api_client
from src.providers.open_ai_client import OpenAI_client
from pydantic import BaseModel
from typing import List, Type
from src.abs.prompt import Prompt as DefaultPromptModel
import asyncio
from src.providers.gemini_client import Gemini_client
from src.providers.grok_client import Grok_client

class aggregator:
    """
    class that handles all the async client classes
    """
    providers: List[api_client]
    def __init__(self, prompt_class: Type[BaseModel]):
        """
        Accept a Pydantic `BaseModel` subclass (prompt_class) so different prompt schemas
        can be used with the aggregator.
        """
        self.prompt_class = prompt_class
        self.providers = [OpenAI_client("gpt-4o-mini"), Gemini_client("gemini-2.5-flash")]
    
    def run_prompt(self, prompt: BaseModel, **kwargs) -> List:
        """
        Run all of the async run methods for all of the providers.
        This function is not async itself to be called by the scripts, but
        it is asynchronous internally

        If one of them returns an error, log it then continue
        """
        print(f"Prompt id: {prompt.id} completed for all models")
        return asyncio.run(self._run_prompt(prompt, **kwargs))

    
    async def _run_prompt(self, prompt: BaseModel, **kwargs) -> List:
        """
        """
        results = await asyncio.gather(*[provider.call(prompt) for provider in self.providers])
        return results

if __name__ == "__main__":
    pass
