"""
AURA API Pipeline - Simple Runner (Legacy)
==========================================

NOTE: For more flexibility, use main_cli.py instead!
      This file is kept for backwards compatibility.

This script runs the pipeline with HARDCODED schemas.

TO CHANGE THE DATASET OR SCHEMAS:
    Option 1: Use CLI (recommended)
        python src/main_cli.py --input-file your_data.json

    Option 2: Edit these lines below:
        Line ~25: Change 'reddit_dataset.json' to your input file
        Line ~26: Change output path if needed
        
    Option 3: Create custom main_*.py file for your experiment
"""

from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.aggregator import aggregator
from src.data_readers.prompt_reader import prompt_reader
from src.abs.prompt import Prompt
from src.abs.structure import AIResponse
import json


# ============================================================================
# CONFIGURATION - EDIT THESE LINES TO CHANGE DATASET/SCHEMAS
# ============================================================================

INPUT_FILE = 'reddit_dataset.json'  # ← Change this to your input file
OUTPUT_FILE = 'outputs/test_no_prompt.json'  # ← Change output path here

# To use custom schemas, uncomment and modify:
# from examples.example_prompts import ExamplePrompt
# from examples.example_responses import ExampleResponse
# PROMPT_CLASS = ExamplePrompt
# RESPONSE_CLASS = ExampleResponse

PROMPT_CLASS = Prompt
RESPONSE_CLASS = AIResponse

# ============================================================================


project_root = Path(__file__).parent.parent
output_path = project_root / OUTPUT_FILE

def main():
    # Initialize aggregator with response schema
    ag = aggregator(response_schema=RESPONSE_CLASS)
    
    # Load prompts
    prompts = prompt_reader(INPUT_FILE)
    
    data = {}

    for prompt in prompts:
        responses = ag.run_prompt(prompt)

        data[prompt.id] = {
            "prompt": prompt.prompt,
            "category": prompt.category,
            "outputs": {}
        }

        for model_name, ai_response in responses:
            # ai_response is now an AIResponse Pydantic object
            data[prompt.id]["outputs"][model_name] = {
                "response": ai_response.response,
                "emotion": ai_response.emotion_classification,
                "ai_risk_assessment": ai_response.risk_assessment,
                "should_continue": ai_response.should_continue,
                "classification": None  # Placeholder for manual/AI classification
            }
            # print(f"Model: {model}, Output: {output}")

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"✓ JSON saved successfully to {output_path}")


if __name__ == "__main__":
    main()