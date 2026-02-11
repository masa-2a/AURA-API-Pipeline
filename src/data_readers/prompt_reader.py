from pathlib import Path
import json
from typing import List
from src.abs.prompt import Prompt


def prompt_reader() -> List[Prompt]:
    """
    returning a list of prompt objects from the JSON input file
    """
    prompts = []
    project_root = Path(__file__).parent.parent.parent
    json_path = project_root / 'input_prompts' / 'prompts.json'
    
    with open(json_path, mode='r') as file:
        data = json.load(file)
        for item in data:
            # construct Prompt using the same ordering used elsewhere: (text, category/emotion, id)
            p = Prompt(item.get('text', ''), item.get('emotion') or item.get('category'), item.get('id'))
            prompts.append(p)
    
    return prompts

if __name__ == "__main__":
    prompts = prompt_reader()
    for prompt in prompts:
        print(prompt)