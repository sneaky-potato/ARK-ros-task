#!/usr/bin/env python
import rospy
import sys
import std_msgs

def start_node(filename):
    rospy.init_node('image_pub')
    rospy.loginfo('image_pub node started')
    pub = rospy.Publisher('filepath', std_msgs.msg.String, queue_size=10)
    while not rospy.is_shutdown():
        pub.publish(filename)
        rospy.Rate(1.0).sleep()  # 1 Hz


if __name__ == '__main__':
    try:
        if(not (sys.argv)[1]):
            print("Usage: rosrun [PACKAGE_NAME] [NODE] [filepath]")
            pass
        start_node( rospy.myargv(argv=sys.argv)[1])
    except rospy.ROSInterruptException:
        pass
