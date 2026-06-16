import pybullet as p
import pybullet_data
import time

# Connect GUI
p.connect(p.GUI)

# Load assets
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Gravity
p.setGravity(0, 0, -9.8)

# Load plane
plane = p.loadURDF("plane.urdf")

# Load robot
robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)

# Load cube
cube = p.loadURDF(
    "cube_small.urdf",
    basePosition=[0.5, 0, 0.02]
)


def move_robot(position, steps=300):
    joint_positions = p.calculateInverseKinematics(
        robot,
        11,
        position
    )

    for i in range(7):
        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            targetPosition=joint_positions[i]
        )

    for _ in range(steps):
        p.stepSimulation()
        time.sleep(1 / 240)


def open_gripper():
    p.setJointMotorControl2(
        robot, 9,
        p.POSITION_CONTROL,
        targetPosition=0.04,
        force=100
    )

    p.setJointMotorControl2(
        robot, 10,
        p.POSITION_CONTROL,
        targetPosition=0.04,
        force=100
    )

    for _ in range(200):
        p.stepSimulation()
        time.sleep(1 / 240)


def close_gripper():
    p.setJointMotorControl2(
        robot, 9,
        p.POSITION_CONTROL,
        targetPosition=0,
        force=100
    )

    p.setJointMotorControl2(
        robot, 10,
        p.POSITION_CONTROL,
        targetPosition=0,
        force=100
    )

    for _ in range(200):
        p.stepSimulation()
        time.sleep(1 / 240)


# 1. Go above cube
move_robot([0.5, 0, 0.18])

# 2. Open gripper
open_gripper()

# 3. Move carefully down
move_robot([0.5, 0, 0.06])

# 4. Close fingers
close_gripper()

# 5. Wait
for _ in range(100):
    p.stepSimulation()
    time.sleep(1 / 240)

# 6. Lift slowly
move_robot([0.5, 0, 0.25], steps=500)

# Keep simulation alive
while True:
    p.stepSimulation()
    time.sleep(1 / 240)