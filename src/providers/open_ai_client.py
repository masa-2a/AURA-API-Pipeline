from openai import OpenAI
from . import OPENAI_API_KEY
from src.abs.client import api_client
import asyncio
from openai import OpenAIError, APIError, RateLimitError, APIConnectionError, Timeout
from src.abs.prompt import Prompt
from src.abs.structure import AIResponse

"""
open ai api calls

test with:
python3 -m src.providers.open_ai_client

"""

class OpenAI_client(api_client):
    
    def __init__(self, model: str, response_schema=None):
        super().__init__(model)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # Import here to avoid circular dependency
        if response_schema is None:
            from src.abs.structure import AIResponse
            response_schema = AIResponse
        self.response_schema = response_schema
    
    async def call(self, prompt: Prompt, **kwargs):
        """
        Make a call asynchronously by running the synchronous SDK call in a 
        background thread. Returns (model_name, AIResponse) tuple.

        additional arguments will be required for rate limiting maybe

        returning a tuple (modelname, AIResponse) so that we know which model outputs what
        when we are saving to the json

        """
        try:
            response = await asyncio.to_thread(
                self.client.responses.parse,
                model=self.model_name,
                input=[
                        {"role": "system", "content": "You are here to provide non-clinical support and make suggestions."}, #system prompt that defines the assistant behavior, maybe change to a specfied prompt
                        {"role": "user", "content": prompt.prompt},
                ],
                text_format=self.response_schema, # Use configurable response schema
                **kwargs
            )

            print(f"Prompt id: {prompt.id} for model: {self.model_name} completed")
            return (self.model_name, response.output_parsed)  # Return the response object

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e} in prompt id: {prompt.id} in OpenAI client")
            # Return default response on error - create instance with default values
            try:
                error_response = self.response_schema()
            except:
                # If can't create default, return dict
                error_response = {"error": f"{type(e).__name__}: {e}"}
            return (self.model_name, error_response)

async def test():
    client = OpenAI_client(model="gpt-4o-mini", prompt_structure=Prompt_structure)   
    prompt = Prompt(id=1, text="Say hello!", category="happy")

    print("Calling API...")
    result = await client.call(prompt)

    print("Result:\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(test())