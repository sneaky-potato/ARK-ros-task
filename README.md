# ARK-ros-task
---
## Problem Statement
You are given 30 files in totality,10 each of types 0 (RGB), 1 (Segmentation) and 2 (Pose). The files are named in the format <id>_<type>.<extension> in individualf olders.
Each image is 256x144 in size. The image data is collected using a projective pinhole camera, which has a horizontal field-of-view (FOV) of 90°. You can assume the distortion parameters to be zero, and the principal point of the image to be at its center. You can also assume the focal length in x and y directions to be equal. The pose data is the position of the camera in the world coordinates in the NED (North, East, Down) coordinate system. It is stored in the form of an orientation quaternion and aposition vector
