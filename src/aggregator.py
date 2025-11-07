import asyncio
from datetime import datetime
from typing import Dict, Any
from src.prompt import Prompt
from src.providers.provider import ProviderResult

class Aggregator:
    def __init__(self, providers):
        self.providers = providers
        self._id = 1

    async def run(self, prompt: Prompt) -> Dict[str, Any]:
        coros = [p.generate(prompt.text) for p in self.providers]
        results: list[ProviderResult] = await asyncio.gather(*coros, return_exceptions=False)

        outputs: Dict[str, str] = {}

        for r in results:
            outputs[r.provider] = r.text if not r.error else f"[ERROR] {r.error}"

        record = {
            "id": self._id,
            "prompt": prompt.text,
            "category": prompt.category,
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
            "outputs": outputs,          # plain text per model
        }
        self._id += 1
        return record