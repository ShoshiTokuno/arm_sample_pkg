#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import actionlib
import math
import random
from geometry_msgs.msg import Point, Pose
from gazebo_msgs.msg import ModelStates
from control_msgs.msg import GripperCommandAction, GripperCommandGoal
from tf.transformations import quaternion_from_euler, euler_from_quaternion

gazebo_model_states = ModelStates()

def callback(msg):
    global gazebo_model_states
    gazebo_model_states = msg

def yaw_of(object_orientation):
    euler = euler_from_quaternion((object_orientation.x, object_orientation.y, object_orientation.z, object_orientation.w))
    return euler[2]

def main():
    global gazebo_model_states

    OBJECT_NAME = "wood_cube_5cm"
    GRIPPER_OPEN = 1.2
    GRIPPER_CLOSE = 0.42
    APPROACH_Z = 0.15
    LEAVE_Z = 0.20
    PICK_Z = 0.12

    sub_model_states = rospy.Subscriber("gazebo/model_states", ModelStates, callback, queue_size=1)
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.4)
    gripper = actionlib.SimpleActionClient("crane_x7/gripper_controller/gripper_cmd", GripperCommandAction)
    gripper.wait_for_server()
    gripper_goal = GripperCommandGoal()
    gripper_goal.command.max_effort = 4.0
    rospy.sleep(1.0)

    while True:
        gripper_goal.command.position = GRIPPER_OPEN
        gripper.send_goal(gripper_goal)
        gripper.wait_for_result(rospy.Duration(1.0))

        arm.set_named_target("home")
        arm.go()
        rospy.sleep(1.0)

        sleep_time = 3.0

        print "Wait" + str(sleep_time) + "secs."
        rospy.sleep(sleep_time)
        print "Start"

        if OBJECT_NAME in gazebo_model_states.name:
            object_index = gazebo_model_states.name.index(OBJECT_NAME)
            object_position = gazebo_model_states.pose[object_index].position
            object_orientation = gazebo_model_states.pose[object_index].orientation
            object_yaw = yaw_of(object_orientation)
            target_pose = Pose()

            #近づく
            target_pose.position.x = object_position.x
            target_pose.position.y = object_position.y
            target_pose.position.z = APPROACH_Z
            q = quaternion_from_euler(-math.pi, 0.0, object_yaw)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to approach an object."
                continue
            rospy.sleep(1.0)

            # 掴みに行く
            target_pose.position.z = PICK_Z
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to grip an object."
                continue
            rospy.sleep(1.0)
            gripper_goal.command.position = GRIPPER_CLOSE
            gripper.send_goal(gripper_goal)
            gripper.wait_for_result(rospy.Duration(1.0))

            # 持ち上げる
            target_pose.position.z = LEAVE_Z;
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to pick up an object."
                continue
            rospy.sleep(1.0)

            target_pose.position.x = 0.25
            target_pose.position.y = 0.0
            target_pose.position.z = 0.25
            q = quaternion_from_euler(0.0, math.pi/2, 0.0)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to approach an object."
                continue
            rospy.sleep(1.0)

            target_pose.position.x = 0.25*math.sin(math.pi/6)
            target_pose.position.z = 0.25*math.cos(math.pi/6) + 0.25
            q = quaternion_from_euler(0.0, math.pi/6, 0.0)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to turn right an object."
                continue
            rospy.sleep(0.1)

            target_pose.position.x = 0.25
            target_pose.position.z = 0.25
            q = quaternion_from_euler(0.0, math.pi/2, 0.0)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to turn right an object."
                continue
            rospy.sleep(0.1)

            target_pose.position.x = 0.25*math.sin(math.pi/6)
            target_pose.position.z = 0.25*math.cos(math.pi/6) + 0.25
            q = quaternion_from_euler(0.0, math.pi/6, 0.0)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to turn right an object."
                continue
            rospy.sleep(0.1)

            target_pose.position.x = 0.25
            target_pose.position.z = 0.25
            q = quaternion_from_euler(0.0, math.pi/2, 0.0)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to turn right an object."
                continue
            rospy.sleep(0.1)

            q = quaternion_from_euler(-math.pi, 0.0, -math.pi/2.0)
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to approach target position."
                continue
            rospy.sleep(1.0)

            target_pose.position.z = PICK_Z
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to place an object."
                continue
            rospy.sleep(1.0)
            gripper_goal.command.position = GRIPPER_OPEN
            gripper.send_goal(gripper_goal)
            gripper.wait_for_result(rospy.Duration(1.0))

            # ハンドを上げる
            target_pose.position.z = LEAVE_Z
            arm.set_pose_target(target_pose)
            if arm.go() is False:
                print "Failed to leave from an object."
                continue
            rospy.sleep(1.0)

            arm.set_named_target("home")
            if arm.go() is False:
                print "Failed to go back to home pose."
                continue
            rospy.sleep(1.0)

            print("Done")

        else:
            print "No objects"

if __name__ == '__main__':
    rospy.init_node("sample6")

    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
