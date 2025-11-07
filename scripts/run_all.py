# run all our apis with utils and aggregation
import asyncio
import json
import argparse
from pathlib import Path

from src.aggregator import Aggregator
from src.providers.openaiprovider import OpenAIProvider
from src.prompt import Prompt

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT_DIR / "outputs" / "outputs.json"

async def main():
    parser = argparse.ArgumentParser(description="Run the AURA pipeline once.")
    parser.add_argument(
        "--prompt",
        required=False,
        default="I feel like everyone around me is moving forward, and I’m stuck.",
        help="Prompt text to send to all providers",
    )
    parser.add_argument(
        "--category",
        required=False,
        default=None,
        help="Optional category label (e.g., sadness, anxiety)",
    )
    args = parser.parse_args()

    # 1) Providers (OpenAI only for now)
    providers = [OpenAIProvider(model="gpt-4o")]

    # 2) Aggregator
    agg = Aggregator(providers)

    # 3) Prompt object
    prompt = Prompt(text=args.prompt, category=args.category)

    # 4) Run once and pretty-print JSON
    result = await agg.run(prompt)

    # 4) Save to outputs/outputs.json (append or create)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)  # make sure outputs/ exists

    # If file exists and has JSON, append to it; else create a new list
    if OUTPUT_PATH.exists():
        try:
            with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if not isinstance(existing, list):
                    existing = [existing]
        except json.JSONDecodeError:
            existing = []
    else:
        existing = []

    existing.append(result)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved output to {OUTPUT_PATH.resolve()}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())