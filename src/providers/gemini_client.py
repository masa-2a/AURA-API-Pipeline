from google import genai
from . import GEMENI_API_KEY
from src.abs.client import api_client
import asyncio
from openai import OpenAIError, APIError, RateLimitError, APIConnectionError, Timeout
from src.abs.prompt import Prompt
from src.abs.structure import Prompt_structure
import json

class Gemini_client(api_client):

    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"
    
    async def call(self, prompt: Prompt, **kwargs):
        try:
            response =  await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt.text,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": Prompt_structure.model_json_schema(),
                },
            )

            if not response.text:
                print("error")
            result = json.loads(response.text)
            response, emotion = result["response"], result["emotion_classification"]

            print(f"Prompt id: {prompt.id} for model {self.model_name} completed")

            return (self.model_name, response, emotion)
        
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e} in prompt id: {prompt.id} in OpenAI client")
            return (self.model_name, f"Error: {type(e).__name__}: {e}", '2')

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
