from world import OBJECTS, LOCATIONS


VALID_ACTIONS = ["pick", "place"]


def validate_task_plan_with_errors(task_plan):
    errors = []

    if not isinstance(task_plan, list):
        errors.append("Task plan must be a list.")
        return False, errors

    if len(task_plan) == 0:
        errors.append("Task plan is empty.")
        return False, errors

    for index, step in enumerate(task_plan, start=1):
        if not isinstance(step, dict):
            errors.append(f"Step {index} must be a dictionary.")
            return False, errors

        if "action" not in step:
            errors.append(f"Step {index} is missing action.")
            return False, errors

        action = step["action"]

        if action not in VALID_ACTIONS:
            errors.append(f"Invalid action in step {index}: {action}")
            errors.append(f"Allowed actions: {', '.join(VALID_ACTIONS)}")
            return False, errors

        if action == "pick":
            if "object" not in step:
                errors.append(f"Pick step {index} is missing object.")
                return False, errors

            object_name = step["object"]

            if object_name not in OBJECTS:
                errors.append(f"Invalid object in step {index}: {object_name}")
                errors.append(f"Available objects: {', '.join(OBJECTS.keys())}")
                return False, errors

        elif action == "place":
            if "location" not in step:
                errors.append(f"Place step {index} is missing location.")
                return False, errors

            location_name = step["location"]

            if location_name not in LOCATIONS:
                errors.append(f"Invalid location in step {index}: {location_name}")
                errors.append(f"Available locations: {', '.join(LOCATIONS.keys())}")
                return False, errors

    return True, ["Task plan validation passed successfully."]


def validate_task_plan(task_plan):
    validation_passed, errors = validate_task_plan_with_errors(task_plan)

    if not validation_passed:
        for error in errors:
            print(error)

    return validation_passed