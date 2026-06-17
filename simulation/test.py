import pybullet as p
import pybullet_data
import time
from robot_controller import *

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

plane = p.loadURDF("plane.urdf")

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)

cube = p.loadURDF(
    "cube_small.urdf",
    basePosition=[0.5, 0, 0.02]
)

initialize(robot, cube)

cube_position, cube_orientation = p.getBasePositionAndOrientation(cube)

print("Cube Position:", cube_position)
print("Cube Orientation:", cube_orientation)

pick_and_place()

while True:
    p.stepSimulation()
    time.sleep(1 / 240)