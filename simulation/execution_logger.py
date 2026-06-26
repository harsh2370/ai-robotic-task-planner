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


def read_recent_logs(limit=5):
    if not LOG_FILE.exists():
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    recent_lines = lines[-limit:]
    logs = []

    for line in recent_lines:
        try:
            logs.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return list(reversed(logs))