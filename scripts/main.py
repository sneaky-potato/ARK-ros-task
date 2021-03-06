#!/usr/bin/env python
import rospy
import std_msgs
import numpy as np
import cv2

def get_distance(point1, point2):
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2]-point2[2])**2)

class Triangulate:
    def __init__(self):
        self.pose = None
        self.corners = None

    def pose_callback(self, msg):
        # "Store" message received.
        projections = np.array(msg.data)
        projections.shape = (10, 3, 4)
        self.pose = projections

    def corners_callback(self, msg):
        # "Store" the message received.
        cornerList = np.array(msg.data)
        cornerList.shape = (10, 2, 2)
        self.corners = cornerList

        # Invoke the function
        self.get_length()
    
    def get_length(self):
        if(self.pose is not None and self.corners is not None): 

            # Data recieved
            for i in range(0, 10, 2):
                # upper_lower_point = cv2.triangulatePoints(self.pose[i], self.pose[i+1], self.corners[i], self.corners[i+1])
                # upper_lower_point[:, 0] = upper_lower_point[:, 0] / upper_lower_point[3, 0]
                # upper_lower_point[:, 1] = upper_lower_point[:, 1] / upper_lower_point[3, 1]
                # diff = (upper_lower_point[:, 0] - upper_lower_point[:, 1])
                print('length=', 0)

    def get_centroid(self):
        pass


def start_node():
    rospy.init_node('main')
    rospy.loginfo('main node started')

    solution_triangulate = Triangulate()
    rospy.Subscriber("corners", std_msgs.msg.Float32MultiArray, solution_triangulate.corners_callback)
    rospy.Subscriber("pose", std_msgs.msg.Float32MultiArray, solution_triangulate.pose_callback)

    # Invoke the solution
    solution_triangulate.get_length()
    solution_triangulate.get_centroid()
    rospy.spin()


if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass