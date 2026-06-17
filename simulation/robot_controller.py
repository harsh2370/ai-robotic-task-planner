import pybullet as p
import time


robot = None
cube = None
grasp_constraint = None

def initialize(robot_id, cube_id):
    global robot, cube

    robot = robot_id
    cube = cube_id


def attach_cube():
    global grasp_constraint

    grasp_constraint = p.createConstraint(
        parentBodyUniqueId=robot,
        parentLinkIndex=11,
        childBodyUniqueId=cube,
        childLinkIndex=-1,
        jointType=p.JOINT_FIXED,
        jointAxis=[0, 0, 0],
        parentFramePosition=[0, 0, 0],
        childFramePosition=[0, 0, 0]
    )

def release_cube():
    global grasp_constraint

    if grasp_constraint is not None:
        p.removeConstraint(grasp_constraint)
        grasp_constraint = None


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



def pick_and_place():
    move_robot([0.5, 0, 0.18])

    open_gripper()

    move_robot([0.5, 0, 0.06])

    close_gripper()

    attach_cube()

    move_robot([0.5, 0, 0.25])

    move_robot([0.3, 0.3, 0.25])

    open_gripper()

    release_cube()