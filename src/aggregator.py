from src.abs.client import api_client
from src.providers.open_ai_client import OpenAI_client
from src.abs.prompt import Prompt
import asyncio
from typing import List

class aggregator:
    """
    class that handles all the async client classes
    """
    providers: List[api_client]
    def __init__(self):
        self.providers = [OpenAI_client("gpt-4o-mini")]
    
    def run_prompt(self, prompt: Prompt, **kwargs) -> List:
        """
        Run all of the async run methods for all of the providers.
        This function is not async itself to be called by the scripts, but
        it is asynchronous internally

        If one of them returns an error, log it then continue
        """
        return asyncio.run(self._run_prompt(prompt, **kwargs))

    
    async def _run_prompt(self, prompt: Prompt, **kwargs) -> List:
        """
        """
        results = await asyncio.gather(*[provider.call(prompt) for provider in self.providers])
        return results

if __name__ == "__main__":
    pass