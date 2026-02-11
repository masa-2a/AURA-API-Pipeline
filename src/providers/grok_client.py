from openai import OpenAI
from . import GROK_API_KEY
from src.abs.client import api_client
import asyncio
from openai import OpenAIError, APIError, RateLimitError, APIConnectionError, Timeout
from src.abs.prompt import Prompt
from src.abs.structure import Prompt_structure

"""
Grok API calls (using OpenAI SDK with xAI base URL)

test with:
python3 -m src.providers.grok_client

"""

class Grok_client(api_client):
    
    def __init__(self, model: str):
        super().__init__(model)
        self.client = OpenAI(
            api_key=GROK_API_KEY,
            base_url="https://api.x.ai/v1"
        )
    
    async def call(self, prompt: Prompt, **kwargs):
        """
        Make a call asynchronously by running the synchronous SDK call in a 
        background thread. Returns the raw response object. This is non-blocking.

        additional arguments will be required for rate limiting maybe

        returning a tuple (modelname, output) so that we know which model outputs what
        when we are saving to the json

        """
        try:
            response = await asyncio.to_thread(
                self.client.responses.parse,
                model=self.model_name,
                input=[
                        {"role": "system", "content": "You are here to provide non-clinical support and make suggestions."}, #system prompt that defines the assistant behavior, maybe change to a specfied prompt
                        {"role": "user", "content": prompt.text},
                ],
                text_format=Prompt_structure, # change to the pydantic class
                **kwargs
            )

            print(f"Prompt id: {prompt.id} for model: {self.model_name} completed")
            return (self.model_name, response.output_parsed.response, response.output_parsed.emotion_classification, response.output_parsed.risk_assessment, response.output_parsed.should_continue)

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e} in prompt id: {prompt.id} in Grok client")
            return (self.model_name, f"Error: {type(e).__name__}: {e}", "error", "unknown", "unknown")

async def test():
    client = Grok_client(model="grok-beta")   
    prompt = Prompt(id=1, text="Say hello!", category="happy")

    print("Calling Grok API...")
    result = await client.call(prompt)

    print("Result:\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(test())
