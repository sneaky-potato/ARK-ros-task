#!/usr/bin/env python
import rospy
from tf.transformations import quaternion_matrix
import std_msgs
import re
import numpy as np


def findvector(msg):
    pose = "".join([str(msg.data), 'Pose/0_2.txt'])
    f = open(pose, "r")
    vector = f.read()
    vector = re.sub('<.*?>', '', vector)
    print(vector)
    dictionary = eval(vector)

    rmat = quaternion_matrix([dictionary['orientation']['w_val'], dictionary['orientation']['x_val'], dictionary['orientation']['y_val'], dictionary['orientation']['z_val']])
    tvec = np.matrix([[dictionary['position']['x_val']], [dictionary['position']['y_val']], [dictionary['position']['z_val']]])
    print(rmat)
    print(tvec)


def start_node():
    rospy.init_node('pose')
    rospy.loginfo('pose node started')
    rospy.Subscriber("filepath", std_msgs.msg.String, findvector)
    rospy.spin()


if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass