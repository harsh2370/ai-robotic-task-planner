def parse_command(command):
    words = command.lower().split()

    if len(words) == 3 and words[0] == "move":
        return [
            {"action": "pick", "object": words[1]},
            {"action": "place", "location": words[2]}
        ]

    print("Invalid command. Use format: move object location")
    return []