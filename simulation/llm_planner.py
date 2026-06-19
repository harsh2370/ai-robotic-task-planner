import json
import requests

from model_config import MODEL_NAME, OLLAMA_URL
from world import OBJECTS, LOCATIONS


def build_prompt(user_command):
    available_objects = list(OBJECTS.keys())
    available_locations = list(LOCATIONS.keys())

    prompt = f"""
You are a robotic task planner.

Your job is to convert a user's natural language command into a JSON task plan.

You must only use these actions:
- pick
- place

Available objects:
{available_objects}

Available locations:
{available_locations}

Rules:
1. Output only valid JSON.
2. Do not explain anything.
3. Do not add extra text.
4. Use this exact format:

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

User command: put the box on the right
Output:
{{
  "steps": [
    {{"action": "pick", "object": "box"}},
    {{"action": "place", "location": "right"}}
  ]
}}

Now convert this command:

User command: {user_command}
Output:
"""

    return prompt


def get_task_plan_from_llm(user_command):
    prompt = build_prompt(user_command)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    raw_output = result["response"]

    try:
        task_plan = json.loads(raw_output)
        return task_plan["steps"]

    except json.JSONDecodeError:
        print("LLM returned invalid JSON:")
        print(raw_output)
        return []