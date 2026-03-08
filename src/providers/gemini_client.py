from google import genai
from . import GEMENI_API_KEY
from src.abs.client import api_client
import asyncio
from openai import OpenAIError, APIError, RateLimitError, APIConnectionError, Timeout
from src.abs.prompt import Prompt
from src.abs.structure import AIResponse
import json

class Gemini_client(api_client):

    def __init__(self, model_name: str, response_schema=None) -> None:
        super().__init__(model_name)
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"
        # Import here to avoid circular dependency
        if response_schema is None:
            from src.abs.structure import AIResponse
            response_schema = AIResponse
        self.response_schema = response_schema
    
    async def call(self, prompt: Prompt, **kwargs):
        try:
            response =  await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt.prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": self.response_schema.model_json_schema(),
                },
            )

            if not response.text:
                print("error")
            
            # Parse JSON response into response object
            result = json.loads(response.text)
            ai_response = self.response_schema(**result)

            print(f"Prompt id: {prompt.id} for model {self.model_name} completed")

            return (self.model_name, ai_response)
        
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e} in prompt id: {prompt.id} in Gemini client")
            try:
                error_response = self.response_schema()
            except:
                error_response = {"error": f"{type(e).__name__}: {e}"}
            return (self.model_name, error_response)

async def test():
    prompt = Prompt(
        id=1,
        text="Im sad :(",
        category="sad"
    )

    client = Gemini_client(model_name="gemini-2.5-flash")

    # call the API
    model_name, response, emotion = await client.call(prompt)

    print("MODEL:", model_name)
    print("RESPONSE:", response)
    print("EMOTION:", emotion)

if __name__ == "__main__":
    asyncio.run(test())
