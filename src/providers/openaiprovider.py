import os, asyncio, json
from typing import Any
from openai import OpenAI
from .provider import Provider, ProviderResult

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _openai_text(resp: Any) -> str:
    try:
        return resp.choices[0].message.content.strip()
    except Exception:
        # fallback if resp already a dict
        try:
            return resp["choices"][0]["message"]["content"].strip()
        except Exception:
            return str(resp)

def _openai_to_jsonable(resp: Any):
    # Try to turn the SDK object into a JSONable dict
    for attr in ("model_dump", "to_dict"):
        fn = getattr(resp, attr, None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass
    # last resort: string
    try:
        return json.loads(str(resp))
    except Exception:
        return str(resp)

class OpenAIProvider(Provider):
    def __init__(self, model: str = "gpt-4o", api_key: str | None = None):
        self.name = model
        self.model = model
        self.api_key = OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    async def generate(self, prompt_text: str, **kwargs) -> ProviderResult:
        #no api key found
        if not self.client:
            return ProviderResult(
                provider=self.name,
                text="generic test response (NO CLIENT)",
            )

        try:
            resp = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": prompt_text}],
                **kwargs
            )
            text = _openai_text(resp)
            raw_json = _openai_to_jsonable(resp)
            # usage fields differ by SDK versions; best-effort capture
            usage = getattr(resp, "usage", None)
            meta = {
                "tokens": {
                    "input": getattr(usage, "prompt_tokens", None),
                    "output": getattr(usage, "completion_tokens", None),
                    "total": getattr(usage, "total_tokens", None),
                }
            }
            return ProviderResult(provider=self.name, text=text)
        except Exception as e:
            return ProviderResult(provider=self.name, text=f"[ERROR] {e}")