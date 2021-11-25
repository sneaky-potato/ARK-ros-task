#!/usr/bin/env python
import rospy
import std_msgs
import numpy as np
import cv2

class Triangulate:
    def __init__(self):
        self.pose = None
        self.corners = None
        #self.ts = message_filters.TimeSynchronizer([self.pose, self.corners], 10)
        #self.ts.registerCallback(self.get_length)

    def pose_callback(self, msg):
        # "Store" message received.
        projections = np.array(msg.data)
        projections.shape = (10, 3, 4)
        self.pose = projections
        #print("------- pose ------")
        #print("pose data=", self.pose)
        #print("corner data=", self.corners)

    def corners_callback(self, msg):
        # "Store" the message received.
        cornerList = np.array(msg.data)
        cornerList.shape = (10, 2, 2)
        self.corners = cornerList
        #print("------- corner ------")
        #print("pose data=", self.pose)
        #print("corner data=", self.corners)
        self.get_length()
    
    def get_length(self):
        #print("pose=", self.pose)
        #print("corner=", self.corners)
        if(self.pose is not None and self.corners is not None): 
            #print("goddit")
            for i in range(0, 10, 2):
                upper_lower_point = cv2.triangulatePoints(self.pose[i], self.pose[i+1], self.corners[i], self.corners[i+1])
                upper_lower_point[:, 0] = upper_lower_point[:, 0] / upper_lower_point[3, 0]
                upper_lower_point[:, 1] = upper_lower_point[:, 1] / upper_lower_point[3, 1]
                diff = (upper_lower_point[:, 0] - upper_lower_point[:, 1])
                print('length=', np.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2))


def start_node():
    rospy.init_node('main')
    rospy.loginfo('main node started')

    solution_triangulate = Triangulate()
    rospy.Subscriber("corners", std_msgs.msg.Float32MultiArray, solution_triangulate.corners_callback)
    rospy.Subscriber("pose", std_msgs.msg.Float32MultiArray, solution_triangulate.pose_callback)
    solution_triangulate.get_length()
    rospy.spin()


if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass