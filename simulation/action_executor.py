from world import OBJECTS, LOCATIONS
from robot_controller import (
    move_robot,
    open_gripper,
    close_gripper,
    attach_object,
    release_object
)


def pick_object(object_name):
    object_position = OBJECTS[object_name]["position"]

    x = object_position[0]
    y = object_position[1]

    move_robot([x, y, 0.18])
    open_gripper()
    move_robot([x, y, 0.06])
    close_gripper()
    attach_object(object_name)
    move_robot([x, y, 0.25])


def place_object(location_name):
    location_position = LOCATIONS[location_name]

    x = location_position[0]
    y = location_position[1]
    z = location_position[2]

    move_robot([x, y, 0.22])
    move_robot([x, y, z])
    open_gripper()
    release_object()

    for _ in range(120):
        move_robot([x, y, 0.18], steps=1)

def execute_action(action):
    if action["action"] == "pick":
        pick_object(action["object"])

    elif action["action"] == "place":
        place_object(action["location"])

    else:
        print("Unknown action:", action["action"])