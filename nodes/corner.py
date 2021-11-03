#!/usr/bin/env python
from numpy.lib.type_check import imag
import rospy
import sys
import std_msgs
import cv2
import numpy as np

def start_node(filename):
    rospy.init_node('croner_pub')
    rospy.loginfo('corner_pub node started')
    pub = rospy.Publisher('corners', std_msgs.msg.Float32MultiArray, queue_size=10)

    image = cv2.imread(filename + '0_1.png')
    print(image.shape)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    # Extracting corners
    dst = cv2.cornerHarris(gray,5,3,0.04)
    # thresholding
    ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
    dst = np.uint8(dst)
    # Connecting potentially redundant corners
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
    print(corners)
    image[dst>0.1*dst.max()]=[0,0,255]

    while not rospy.is_shutdown():
        data_to_send = std_msgs.msg.Float32MultiArray()  # the data to be sent, initialise the array
        
        data_to_send.data = corners.flatten()
        pub.publish(data_to_send)
        rospy.Rate(1.0).sleep()  # 1 Hz


if __name__ == '__main__':
    try:
        if(not (sys.argv)[1]):
            print("Usage: rosrun [PACKAGE_NAME] [NODE] [filepath]")
            pass
        start_node( rospy.myargv(argv=sys.argv)[1])
    except rospy.ROSInterruptException:
        pass
