#!/usr/bin/env python
import rospy
import sys
import std_msgs
import cv2
import numpy as np

def start_node(filename):
    rospy.init_node('croner_pub')
    rospy.loginfo('corner_pub node started')
    pub = rospy.Publisher('corners', std_msgs.msg.Float32MultiArray, queue_size=10)
    
    if(filename[-1] != '/'): filename += '/'
    cornerlist = np.zeros((10, 2, 2))
    for i in range(10):
        image = cv2.imread(filename + str(i) + '_1.png')
        print(image.shape)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = 1.0 - gray / 255.0

        thresh = cv2.threshold(gray, 0.5, 1.0, cv2.THRESH_BINARY)[1]
        thresh = 255.0 * thresh
        thresh = np.uint8(thresh)

        # Extracting corners
        dst = cv2.cornerHarris(thresh,5,7,0.02)
        
        # thresholding
        ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
        dst = np.uint8(dst)
        output = cv2.connectedComponentsWithStats(dst, 4, cv2.CV_32S)
        
        centroids = output[3][1:,:]
        cornerlist[i, :, :] = np.matrix([[corners[minind, 0], corners[maxind, 0]], [corners[minind, 1], corners[maxind, 1]]])
        #print(corners)
        image[dst>0.1*dst.max()]=[0,0,255]

    while not rospy.is_shutdown():
        data_to_send = std_msgs.msg.Float32MultiArray()  # the data to be sent, initialise the array
        
        data_to_send.data = cornerlist.flatten()
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
