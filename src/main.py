from pathlib import Path
from src.aggregator import aggregator
from src.data_readers.prompt_reader import prompt_reader
import json


project_root = Path(__file__).parent.parent
# output_path = project_root / 'outputs' / 'output_test.json'

output_path = project_root / 'outputs' / 'test_no_prompt.json'
output_path_str = str(output_path)

def main():
    ag = aggregator()
    prompts = prompt_reader()
    data = {}

    for prompt in prompts:
        responses = ag.run_prompt(prompt)

        data[prompt.id] = {
            "prompt": prompt.prompt,
            "category": prompt.category,
            "outputs": {}
        }

        for model, response, emotion in responses:
            
            # output = json.dumps(outputJSON)
            # get and split specific response parts from response JSONOBJ

            data[prompt.id]["outputs"][model] = {
                "response": response,
                "emotion": emotion
            }
            # print(f"Model: {model}, Output: {output}")

    with open(output_path_str, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print("JSON save succesful")


if __name__ == "__main__":
    main()