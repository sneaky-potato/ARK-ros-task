#!/usr/bin/env python
import rospy
import std_msgs
import numpy as np

class Triangulate:
    def __init__(self):
        self.pose = None
        self.corners = None

    def pose_callback(self, msg):
        # "Store" message received.
        self.pose = msg

    def corners_callback(self, msg):
        # "Store" the message received.
        self.corners = msg


def start_node():
    rospy.init_node('main')
    rospy.loginfo('main node started')

    solution_triangulate = Triangulate()
    rospy.Subscriber("corners", std_msgs.msg.Float32MultiArray, solution_triangulate.corners_callback)
    rospy.Subscriber("pose", std_msgs.msg.Float32MultiArray, solution_triangulate.pose_callback)

    rospy.spin()


if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass