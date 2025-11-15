import sys
from pathlib import Path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from abs.prompt import Prompt
import json
from typing import List

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
            p = Prompt(item['text'], item['emotion'], item['id'])
            prompts.append(p)
    
    return prompts

if __name__ == "__main__":
    prompts = prompt_reader()
    for prompt in prompts:
        print(prompt)