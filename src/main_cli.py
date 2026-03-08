"""
AURA API Pipeline - CLI Runner
==============================

Run experiments with different input/output schemas via command line.

USAGE:
    python src/main_cli.py \\
        --prompt-module reddit_data.reddit_prompt \\
        --prompt-class RedditPrompt \\
        --response-module reddit_data.reddit_response \\
        --response-class MentalHealthResponse \\
        --input-file reddit_dataset.json \\
        --output-file outputs/reddit_results.json

EXAMPLES:
    # Mental health dataset with Reddit schemas (recommended)
    python src/main_cli.py \\
        --prompt-module reddit_data.reddit_prompt \\
        --prompt-class RedditPrompt \\
        --response-module reddit_data.reddit_response \\
        --response-class MentalHealthResponse
    
    # Or use default (uses src.abs.prompt.Prompt and src.abs.structure.AIResponse)
    python src/main_cli.py

    # Custom dataset with custom schemas
    python src/main_cli.py \\
        --prompt-module your_folder.custom_prompt \\
        --prompt-class CustomPrompt \\
        --response-module your_folder.custom_response \\
        --response-class CustomResponse \\
        --input-file my_data.json \\
        --output-file outputs/my_results.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Type
from pydantic import BaseModel
import importlib

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.aggregator import aggregator


def import_class(module_path: str, class_name: str) -> Type[BaseModel]:
    """
    Dynamically import a class from a module path.
    
    Args:
        module_path: Dot-notation path like 'src.abs.prompt'
        class_name: Name of the class to import like 'Prompt'
    
    Returns:
        The imported class
    """
    try:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls
    except (ImportError, AttributeError) as e:
        print(f"Error importing {class_name} from {module_path}: {e}")
        sys.exit(1)


def load_prompts(input_file: str, prompt_class: Type[BaseModel]) -> List[BaseModel]:
    """
    Load prompts from JSON file and instantiate with prompt_class.
    
    Args:
        input_file: Filename in input_prompts/ directory
        prompt_class: Pydantic class to instantiate
    
    Returns:
        List of prompt objects
    """
    json_path = project_root / 'input_prompts' / input_file
    
    if not json_path.exists():
        print(f"Error: Input file not found: {json_path}")
        sys.exit(1)
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    prompts = []
    for item in data:
        try:
            prompt = prompt_class(**item)
            prompts.append(prompt)
        except Exception as e:
            print(f"Warning: Failed to parse prompt {item.get('id', '?')}: {e}")
    
    print(f"✓ Loaded {len(prompts)} prompts from {input_file}")
    return prompts


def run_pipeline(
    prompts: List[BaseModel],
    response_schema: Type[BaseModel],
    output_file: str
):
    """
    Run the aggregator pipeline and save results.
    
    Args:
        prompts: List of prompt objects
        response_schema: Pydantic class for AI responses
        output_file: Output file path
    """
    # Initialize aggregator with response schema
    ag = aggregator(response_schema=response_schema)
    
    data = {}
    
    for prompt in prompts:
        print(f"\nProcessing prompt {prompt.id}...")
        responses = ag.run_prompt(prompt)
        
        # Store prompt data (all fields from Pydantic model)
        data[prompt.id] = {
            "prompt_data": prompt.model_dump(),
            "outputs": {}
        }
        
        # Store each provider's response
        for model_name, ai_response in responses:
            # Use model_dump() to automatically serialize any Pydantic model
            data[prompt.id]["outputs"][model_name] = ai_response.model_dump()
    
    # Save results
    output_path = project_root / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✓ Results saved to {output_path}")
    print(f"✓ Processed {len(data)} prompts")


def main():
    parser = argparse.ArgumentParser(
        description='Run AURA API Pipeline with custom input/output schemas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--prompt-module',
        default='src.abs.prompt',
        help='Module path for prompt class (default: src.abs.prompt)'
    )
    
    parser.add_argument(
        '--prompt-class',
        default='Prompt',
        help='Prompt class name (default: Prompt)'
    )
    
    parser.add_argument(
        '--response-module',
        default='src.abs.structure',
        help='Module path for response class (default: src.abs.structure)'
    )
    
    parser.add_argument(
        '--response-class',
        default='AIResponse',
        help='Response class name (default: AIResponse)'
    )
    
    parser.add_argument(
        '--input-file',
        default='reddit_dataset.json',
        help='Input JSON file in input_prompts/ (default: reddit_dataset.json)'
    )
    
    parser.add_argument(
        '--output-file',
        default='outputs/test_no_prompt.json',
        help='Output file path (default: outputs/test_no_prompt.json)'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("AURA API Pipeline - CLI Runner")
    print("="*60)
    print(f"Prompt Schema:   {args.prompt_module}.{args.prompt_class}")
    print(f"Response Schema: {args.response_module}.{args.response_class}")
    print(f"Input File:      {args.input_file}")
    print(f"Output File:     {args.output_file}")
    print("="*60)
    
    # Import schemas
    prompt_class = import_class(args.prompt_module, args.prompt_class)
    response_class = import_class(args.response_module, args.response_class)
    
    # Load data
    prompts = load_prompts(args.input_file, prompt_class)
    
    # Run pipeline
    run_pipeline(prompts, response_class, args.output_file)


if __name__ == "__main__":
    main()
