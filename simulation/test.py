import pybullet as p
import pybullet_data
import time

from robot_controller import initialize
from action_executor import execute_action
from world import OBJECTS

import json
from command_runner import parse_command
from llm_planner import get_task_plan_from_llm
from plan_validator import validate_task_plan


p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

plane = p.loadURDF("plane.urdf")

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)

loaded_objects = {}

for object_name, object_data in OBJECTS.items():
    loaded_objects[object_name] = p.loadURDF(
        object_data["urdf"],
        basePosition=object_data["position"]
    )
    print(f"{object_name} loaded at {object_data['position']}")

tray_visual = p.createVisualShape(
    shapeType=p.GEOM_CYLINDER,
    radius=0.16,
    length=0.005
)

# =========================
# TRAY BASE
# =========================

tray_base_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[0.10, 0.10, 0.01]
)

tray_base_collision = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[0.10, 0.10, 0.01]
)

p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=tray_base_collision,
    baseVisualShapeIndex=tray_base_visual,
    basePosition=[0.75, 0.35, 0.01]
)

# =========================
# TRAY WALLS
# =========================

wall_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[0.10, 0.01, 0.03]
)

wall_collision = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[0.10, 0.01, 0.03]
)

# Front wall
p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=wall_collision,
    baseVisualShapeIndex=wall_visual,
    basePosition=[0.75, 0.45, 0.04]
)

# Back wall
p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=wall_collision,
    baseVisualShapeIndex=wall_visual,
    basePosition=[0.75, 0.25, 0.04]
)

# Left wall
side_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[0.01, 0.10, 0.03]
)

side_collision = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[0.01, 0.10, 0.03]
)

p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=side_collision,
    baseVisualShapeIndex=side_visual,
    basePosition=[0.65, 0.35, 0.04]
)

# Right wall
p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=side_collision,
    baseVisualShapeIndex=side_visual,
    basePosition=[0.85, 0.35, 0.04]
)
initialize(robot, loaded_objects)
PLANNER_MODE = "llm"
# Options:
# "rule_based" -> uses our simple command parser
# "llm"        -> uses Qwen through Ollama

command = input("Enter command: ")

if PLANNER_MODE == "llm":
    task_plan = get_task_plan_from_llm(command)
else:
    task_plan = parse_command(command)

print("\nGenerated Task Plan:")
print(json.dumps({"steps": task_plan}, indent=4))

if validate_task_plan(task_plan):
    for action in task_plan:
        execute_action(action)
else:
    print("Task plan validation failed. Robot will not execute.")

while True:
    p.stepSimulation()
    time.sleep(1 / 240)