from pathlib import Path
from src.aggregator import aggregator
from src.data_readers.prompt_reader import prompt_reader
from src.abs.prompt import Prompt
import json


project_root = Path(__file__).parent.parent
# output_path = project_root / 'outputs' / 'output_test.json'

output_path = project_root / 'outputs' / 'test_no_prompt.json'
output_path_str = str(output_path)

def main():
    '''
    this is the change basically, allows us to change the master prompt depending on
    the datset / goal we want.
    '''
    ag = aggregator(Prompt)
    prompts = prompt_reader()
    data = {}

    for prompt in prompts:
        responses = ag.run_prompt(prompt)

        data[prompt.id] = {
            "prompt": prompt.prompt,
            "category": prompt.category,
            "risk_level": prompt.risk_level,  # NEW: Include risk level
            "outputs": {}
        }

        for model, response, emotion, risk_assessment, should_continue in responses:
            
            # output = json.dumps(outputJSON)
            # get and split specific response parts from response JSONOBJ

            data[prompt.id]["outputs"][model] = {
                "response": response,
                "emotion": emotion,
                "ai_risk_assessment": risk_assessment,  # NEW: AI's risk assessment
                "should_continue": should_continue,  # NEW: AI's decision to proceed/deflect/stop
                "classification": None  # NEW: Placeholder for manual/AI classification
            }
            # print(f"Model: {model}, Output: {output}")

    with open(output_path_str, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print("JSON save succesful")


if __name__ == "__main__":
    main()
