import json
from datetime import datetime
from pathlib import Path


LOG_FILE = Path(__file__).parent / "execution_logs.jsonl"


def log_execution(command, planner_used, task_plan, validation_passed):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "command": command,
        "planner_used": planner_used,
        "task_plan": task_plan,
        "validation_passed": validation_passed
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")