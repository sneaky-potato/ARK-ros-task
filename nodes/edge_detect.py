#!/usr/bin/env python
import rospy

# known pump geometry
#  - units are pixels (of half-size image)
PUMP_DIAMETER = 360
PISTON_DIAMETER = 90
PISTON_COUNT = 7

def start_node():
    rospy.init_node('edge_detect')
    rospy.loginfo('edge_detect node started')

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass