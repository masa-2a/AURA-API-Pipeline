# AURA API-Pipeline

## Purpose

The pipeline aggregates outputs from different LLM models and stores them in a JSON file.

The current models that have been implemented in the pipeline are: Grok, ChatGPT, and Gemini

## Usage

### Model details

Each of the APIs has its own file in the providers directory. Here, the Model type can be changed.

### Input prompts and Outputs

The inputs are a JSON file with keys text, emotion classifier, and a unique prompt ID. These are input as prompt classes to each of the providers.

The structure of the prompts is determined by the pydantic basemodel class found in the structure file.

The output is also in JSON format, which is categorised by each prompts unique ID. There, the input prompt as well as the structured outputs from each of the models are nested.

### Extension

More models can be implemented by creating more api_client classes and adding them to the aggregator. Different outputs and output structure can also be implemented by editing the structure and prompt classes respectively in the abs directory.

### Running the script

The script can be run by running main.py as a package. Prompt completions and errors will be printed to the terminal, errors will not be retried and can be individually retried after the completion of the rest of the prompts. JSON saving only occurs at the end of the script.