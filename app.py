from flask import Flask, render_template, request
import json
import sys
from pathlib import Path

import subprocess

# Add simulation folder to Python path
BASE_DIR = Path(__file__).parent
SIMULATION_DIR = BASE_DIR / "simulation"
sys.path.append(str(SIMULATION_DIR))

from command_runner import parse_command
from llm_planner import get_task_plan_from_llm
from plan_validator import validate_task_plan, validate_task_plan_with_errors
from execution_logger import log_execution, read_recent_logs
from world import OBJECTS, LOCATIONS 


app = Flask(__name__)

def get_object_specs():
    object_specs = []

    for object_name, object_data in OBJECTS.items():
        shape = object_data["shape"]

        if shape == "cylinder":
            size_info = f"radius: {object_data['radius']}, height: {object_data['height']}"
        elif shape == "box":
            size_info = f"half extents: {object_data['half_extents']}"
        else:
            size_info = "custom shape"

        object_specs.append({
            "name": object_name,
            "shape": shape,
            "size_info": size_info
        })

    return object_specs

PLANNER_MODE = "llm"


def generate_task_plan(command):
    planner_used = PLANNER_MODE

    if PLANNER_MODE == "llm":
        task_plan = get_task_plan_from_llm(command)

        if not task_plan:
            planner_used = "rule_based_fallback"
            task_plan = parse_command(command)
    else:
        task_plan = parse_command(command)

    validation_passed, validation_messages = validate_task_plan_with_errors(task_plan)

    log_execution(
        command=command,
        planner_used=planner_used,
        task_plan=task_plan,
        validation_passed=validation_passed
    )

    return planner_used, task_plan, validation_passed, validation_messages

def launch_simulation(command):
    test_file = SIMULATION_DIR / "test.py"

    subprocess.Popen(
        [
            sys.executable,
            str(test_file),
            command
        ],
        cwd=str(BASE_DIR),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        command = request.form.get("command")
        action = request.form.get("action")
        print("Frontend action received:", action)

        planner_used, task_plan, validation_passed, validation_messages = generate_task_plan(command)

        execution_status = None

        if action == "execute":
            if validation_passed:
                launch_simulation(command)
                execution_status = "Simulation started successfully in PyBullet."
            else:
                execution_status = "Simulation not started because validation failed."

        result = {
            "command": command,
            "planner_used": planner_used,
            "task_plan": json.dumps({"steps": task_plan}, indent=4),
            "validation_passed": validation_passed,
            "validation_messages": validation_messages,
            "execution_status": execution_status
        }
    recent_logs = read_recent_logs()
    return render_template(
    "index.html",
    result=result,
    recent_logs=recent_logs,
    objects=list(OBJECTS.keys()),
    locations=list(LOCATIONS.keys()),
    object_specs=get_object_specs()
)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)