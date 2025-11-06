from openai import OpenAI
from . import OPENAI_API_KEY
from abs import api_client
import asyncio

"""
open ai api calls
"""

class OpenAI_client(api_client):
    
    def __init__(self, model: str):
        super().__init__(model)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    async def call(self, prompt: str, **kwargs):
        """
        Make a call asynchronously by running the synchronous SDK call in a 
        background thread. Returns the raw response object. This is non-blocking.

        additional arguments will be required for rate limiting maybe
        """
        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
            )

        return response