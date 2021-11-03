#!/usr/bin/env python
import rospy
from tf.transformations import quaternion_matrix
import std_msgs
import re
import sys
import numpy as np

def start_node(filepath):
    rospy.init_node('pose_pub')
    rospy.loginfo('pose_pub node started')
    pub = rospy.Publisher('pose', std_msgs.msg.Float32MultiArray, queue_size=10)

    if(filepath[-1] != '/'): filepath += '/'
    projections = np.zeros((10, 3, 4))
    print(projections.shape)
    for i in range(10):
        f = open(filepath + str(i) + '_2.txt', "r")
        vector = f.read()
        vector = re.sub('<.*?>', '', vector)
        dictionary = eval(vector)

        rmat = quaternion_matrix([dictionary['orientation']['w_val'], dictionary['orientation']['x_val'], dictionary['orientation']['y_val'], dictionary['orientation']['z_val']])
        tvec = np.matrix([[dictionary['position']['x_val']], [dictionary['position']['y_val']], [dictionary['position']['z_val']]])
        rmat[:3, 3:4] += tvec

        extrinsic = rmat

        f_x = 256 // 2
        f_y = f_x
        c_x = 256 // 2
        c_y = 144 // 2

        intrinsic = np.matrix([[f_x, 0, c_x, 0], [0, f_y, c_y, 0], [0, 0, 1, 0]])

        projection = np.matmul(intrinsic, extrinsic)
        print(projection)
        projections[i, :, :] = projection
    while not rospy.is_shutdown():
        data_to_send = std_msgs.msg.Float32MultiArray()  # the data to be sent, initialise the array
        
        data_to_send.data = projections.flatten()
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