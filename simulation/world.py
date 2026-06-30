OBJECTS = {
    "bottle": {
        "shape": "cylinder",
        "radius": 0.035,
        "height": 0.14,
        "position": [0.45, -0.30, 0.07],
        "color": [0.1, 0.45, 1.0, 1],
        "pick_height": 0.10
    },

    "cup": {
        "shape": "cylinder",
        "radius": 0.045,
        "height": 0.08,
        "position": [0.50, -0.10, 0.04],
        "color": [1.0, 0.55, 0.1, 1],
        "pick_height": 0.07
    },

    "box": {
        "shape": "box",
        "half_extents": [0.045, 0.045, 0.045],
        "position": [0.50, 0.12, 0.045],
        "color": [0.65, 0.35, 1.0, 1],
        "pick_height": 0.08
    },

    "spoon": {
        "shape": "box",
        "half_extents": [0.085, 0.015, 0.01],
        "position": [0.45, 0.30, 0.01],
        "color": [0.85, 0.85, 0.85, 1],
        "pick_height": 0.035
    },

    "plate": {
        "shape": "cylinder",
        "radius": 0.075,
        "height": 0.015,
        "position": [0.60, 0.22, 0.008],
        "color": [0.95, 0.9, 0.45, 1],
        "pick_height": 0.035
    }
}


LOCATIONS = {
    "tray": [0.75, 0.35, 0.07],
    "center": [0.40, 0.00, 0.02],
    "left": [0.35, 0.35, 0.02],
    "right": [0.35, -0.35, 0.02],
    "front": [0.65, 0.00, 0.02],
    "back": [0.25, 0.00, 0.02]
}