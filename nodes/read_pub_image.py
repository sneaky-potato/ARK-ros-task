#!/usr/bin/env python
import rospy
import sys
import cv2

def start_node(filename):
    rospy.init_node('image_pub')
    rospy.loginfo('image_pub node started')
    img = cv2.imread(filename)
    cv2.imshow("image", img)
    cv2.waitKey(2000)

if __name__ == '__main__':
    try:
        start_node( rospy.myargv(argv=sys.argv)[1] )
    except rospy.ROSInterruptException:
        pass
