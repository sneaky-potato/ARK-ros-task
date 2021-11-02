#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def showImage(img):
    cv2.imshow('image', img)
    cv2.waitKey(1)

def process_image(msg):
    try:
       pass
    except Exception as err:
        print(err)
    bridge = CvBridge()
    # converting Image object to cv2 image matrix
    orig = bridge.imgmsg_to_cv2(msg, "bgr8")
    orig = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    drawImg = orig
    # show results
    showImage(drawImg)


def start_node():
    rospy.init_node('edge_detect')
    rospy.loginfo('edge_detect node started')
    # Sending image to process_image function
    rospy.Subscriber("image", Image, process_image)
    rospy.spin()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass