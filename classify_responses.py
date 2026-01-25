from pathlib import Path
import json
import sys

def classify_responses(json_file_path: str):
    """
    Interactive tool to classify model responses as success or fail.
    Displays response, AI risk assessment, and should_continue decision,
    then prompts user for manual classification.
    """
    
    # Load the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {json_file_path}")
        return
    
    print("=" * 80)
    print("RESPONSE CLASSIFICATION TOOL")
    print("=" * 80)
    print("\nInstructions:")
    print("- Review each response")
    print("- Type 'success' or 'fail' to classify")
    print("- Type 'skip' to leave unclassified")
    print("- Type 'quit' to save and exit")
    print("=" * 80)
    
    modified = False
    
    # Iterate through each prompt
    for prompt_id in sorted(data.keys(), key=int):
        prompt_data = data[prompt_id]
        
        print(f"\n{'='*80}")
        print(f"PROMPT ID: {prompt_id}")
        print(f"{'='*80}")
        print(f"Prompt: {prompt_data['prompt']}")
        print(f"Category: {prompt_data['category']}")
        print(f"Risk Level: {prompt_data.get('risk_level', 'N/A')}")
        print(f"{'-'*80}")
        
        # Iterate through each model's response
        for model_name, model_output in prompt_data['outputs'].items():
            print(f"\n*** MODEL: {model_name} ***\n")
            
            # Display response details
            print(f"Response:")
            print(f"{model_output['response']}\n")
            print(f"AI Risk Assessment: {model_output.get('ai_risk_assessment', 'N/A')}")
            print(f"Should Continue: {model_output.get('should_continue', 'N/A')}")
            print(f"Emotion: {model_output.get('emotion', 'N/A')}")
            
            current_classification = model_output.get('classification')
            if current_classification:
                print(f"Current Classification: {current_classification}")
            
            # Prompt for classification
            while True:
                user_input = input("\nClassification (success/fail/skip/quit): ").strip().lower()
                
                if user_input == 'quit':
                    print("\nSaving and exiting...")
                    if modified:
                        with open(json_file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)
                        print(f"✓ Saved classifications to {json_file_path}")
                    else:
                        print("No changes made.")
                    return
                
                elif user_input == 'skip':
                    print("Skipped.")
                    break
                
                elif user_input in ['success', 'fail']:
                    model_output['classification'] = user_input
                    modified = True
                    print(f"✓ Classified as: {user_input}")
                    break
                
                else:
                    print("Invalid input. Please enter 'success', 'fail', 'skip', or 'quit'.")
            
            if user_input == 'quit':
                return
            
            print(f"{'-'*80}")
    
    # Save at the end
    if modified:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n✓ All classifications saved to {json_file_path}")
    else:
        print("\nNo classifications made.")
    
    print("\nClassification complete!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python classify_responses.py <path_to_json_file>")
        print("\nExample:")
        print("  python classify_responses.py outputs/test_no_prompt.json")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    classify_responses(json_file_path)


if __name__ == "__main__":
    main()
