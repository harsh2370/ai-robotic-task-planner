from world import OBJECTS, LOCATIONS


VALID_ACTIONS = ["pick", "place"]


def validate_task_plan(task_plan):
    if not isinstance(task_plan, list):
        print("Invalid plan: Task plan must be a list.")
        return False

    for step in task_plan:
        if "action" not in step:
            print("Invalid step: Missing action.")
            return False

        action = step["action"]

        if action not in VALID_ACTIONS:
            print(f"Invalid action: {action}")
            return False

        if action == "pick":
            if "object" not in step:
                print("Invalid pick step: Missing object.")
                return False

            if step["object"] not in OBJECTS:
                print(f"Invalid object: {step['object']}")
                print("Available objects:", list(OBJECTS.keys()))
                return False

        elif action == "place":
            if "location" not in step:
                print("Invalid place step: Missing location.")
                return False

            if step["location"] not in LOCATIONS:
                print(f"Invalid location: {step['location']}")
                print("Available locations:", list(LOCATIONS.keys()))
                return False

    return True