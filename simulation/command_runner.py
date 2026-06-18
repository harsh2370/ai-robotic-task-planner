from world import OBJECTS, LOCATIONS


def parse_command(command):
    command = command.lower()

    # Remove simple extra words
    words = command.replace(".", "").replace(",", "").split()

    available_objects = list(OBJECTS.keys())
    available_locations = list(LOCATIONS.keys())

    detected_object = None
    detected_location = None

    # Detect object name from command
    for obj in available_objects:
        if obj in words:
            detected_object = obj
            break

    # Detect location name from command
    for loc in available_locations:
        if loc in words:
            detected_location = loc
            break

    # Detect action words
    move_words = ["move", "place", "put", "bring", "transfer"]

    detected_action = None

    for word in words:
        if word in move_words:
            detected_action = "move"
            break

    # Convert natural command into task plan
    if detected_action == "move" and detected_object and detected_location:
        return [
            {
                "action": "pick",
                "object": detected_object
            },
            {
                "action": "place",
                "location": detected_location
            }
        ]

    print("Could not understand command.")
    print("Available objects:", available_objects)
    print("Available locations:", available_locations)
    print("Example commands:")
    print("- move bottle tray")
    print("- move the bottle to the tray")
    print("- place cup left")
    print("- put the box in the right")

    return []