import json
import requests

from model_config import MODEL_NAME, OLLAMA_URL
from world import OBJECTS, LOCATIONS


def build_prompt(user_command):
    available_objects = list(OBJECTS.keys())
    available_locations = list(LOCATIONS.keys())

    prompt = f"""
You are a robotic task planner.

Convert the user's natural language command into a JSON task plan.

Allowed actions:
- pick
- place

Available objects:
{available_objects}

Available locations:
{available_locations}

Rules:
1. Output only valid JSON.
2. Do not explain anything.
3. Do not add markdown.
4. Do not add extra text.
5. Use only available objects and locations.

Required JSON format:
{{
  "steps": [
    {{"action": "pick", "object": "object_name"}},
    {{"action": "place", "location": "location_name"}}
  ]
}}

Examples:

User command: move the bottle to the tray
Output:
{{
  "steps": [
    {{"action": "pick", "object": "bottle"}},
    {{"action": "place", "location": "tray"}}
  ]
}}

User command: place the cup on the left
Output:
{{
  "steps": [
    {{"action": "pick", "object": "cup"}},
    {{"action": "place", "location": "left"}}
  ]
}}

Now convert this command:

User command: {user_command}
Output:
"""

    return prompt


def extract_json_from_text(text):
    text = text.strip()

    # Remove markdown code block markers if the model adds them
    text = text.replace("```json", "")
    text = text.replace("```", "")

    start_index = text.find("{")
    end_index = text.rfind("}")

    if start_index == -1 or end_index == -1:
        print("No JSON object found in LLM output.")
        return None

    json_text = text[start_index:end_index + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError:
        print("Could not parse JSON from LLM output.")
        print("Extracted text was:")
        print(json_text)
        return None


def get_task_plan_from_llm(user_command):
    prompt = build_prompt(user_command)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

    except requests.exceptions.RequestException as error:
        print("Could not connect to Ollama.")
        print(error)
        return []

    result = response.json()
    raw_output = result.get("response", "")

    print("\nRaw LLM Output:")
    print(raw_output)

    parsed_output = extract_json_from_text(raw_output)

    if parsed_output is None:
        return []

    if "steps" not in parsed_output:
        print("Invalid LLM output: Missing 'steps' key.")
        return []

    if not isinstance(parsed_output["steps"], list):
        print("Invalid LLM output: 'steps' must be a list.")
        return []

    return parsed_output["steps"]