import pybullet as p
import time

robot = None
objects = None
grasp_constraint = None
current_object = None


def initialize(robot_id, loaded_objects):
    global robot, objects
    robot = robot_id
    objects = loaded_objects


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
    p.setJointMotorControl2(robot, 9, p.POSITION_CONTROL, targetPosition=0.04, force=100)
    p.setJointMotorControl2(robot, 10, p.POSITION_CONTROL, targetPosition=0.04, force=100)

    for _ in range(200):
        p.stepSimulation()
        time.sleep(1 / 240)


def close_gripper():
    p.setJointMotorControl2(robot, 9, p.POSITION_CONTROL, targetPosition=0, force=100)
    p.setJointMotorControl2(robot, 10, p.POSITION_CONTROL, targetPosition=0, force=100)

    for _ in range(200):
        p.stepSimulation()
        time.sleep(1 / 240)


def attach_object(object_name):
    global grasp_constraint, current_object

    current_object = objects[object_name]

    grasp_constraint = p.createConstraint(
        parentBodyUniqueId=robot,
        parentLinkIndex=11,
        childBodyUniqueId=current_object,
        childLinkIndex=-1,
        jointType=p.JOINT_FIXED,
        jointAxis=[0, 0, 0],
        parentFramePosition=[0, 0, 0],
        childFramePosition=[0, 0, 0]
    )


def release_object():
    global grasp_constraint, current_object

    if grasp_constraint is not None:
        p.removeConstraint(grasp_constraint)
        grasp_constraint = None
        current_object = None