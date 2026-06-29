from world import OBJECTS, LOCATIONS


ACTION_WORDS = [
    "move",
    "place",
    "put",
    "bring",
    "transfer",
    "keep",
    "shift",
    "take"
]


OBJECT_ALIASES = {
    "bottle": ["bottle", "water bottle"],
    "cup": ["cup", "glass", "mug"],
    "box": ["box", "cube", "block"]
}


LOCATION_ALIASES = {
    "tray": ["tray", "container", "basket", "holder"],
    "left": ["left", "left side", "left area"],
    "right": ["right", "right side", "right area"],
    "center": ["center", "middle", "centre"]
}


def clean_command(command):
    command = command.lower()

    symbols = [".", ",", "!", "?", "\"", "'"]

    for symbol in symbols:
        command = command.replace(symbol, "")

    return command


def detect_object(command):
    for object_name, aliases in OBJECT_ALIASES.items():
        for alias in aliases:
            if alias in command and object_name in OBJECTS:
                return object_name

    return None


def detect_location(command):
    for location_name, aliases in LOCATION_ALIASES.items():
        for alias in aliases:
            if alias in command and location_name in LOCATIONS:
                return location_name

    return None


def detect_action(command):
    words = command.split()

    for word in words:
        if word in ACTION_WORDS:
            return "move"

    return None


def parse_command(command):
    command = clean_command(command)

    detected_action = detect_action(command)
    detected_object = detect_object(command)
    detected_location = detect_location(command)

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
    print("Detected action:", detected_action)
    print("Detected object:", detected_object)
    print("Detected location:", detected_location)
    print("Available objects:", list(OBJECTS.keys()))
    print("Available locations:", list(LOCATIONS.keys()))
    print("Example commands:")
    print("- move the bottle to the tray")
    print("- keep the bottle in the container")
    print("- shift the cup to the left side")
    print("- take the box and place it on the right")

    return []