"""
    提供各类转换
"""
import numpy as np

def euler2RM(euler):
    """

    :param euler:
    :return:
    """
    sinP, cosP = np.sin(euler[0]), np.cos(euler[0])
    sinTheta, cosTheta = np.sin(euler[1]), np.cos(euler[1])
    sinC, cosC = np.sin(euler[2]), np.cos(euler[2])

    rm_x = np.array([1, 0, 0, 0, cosP, -sinP, 0, sinP, cosP]).reshape((3, 3))
    rm_y = np.array([cosTheta, 0, sinTheta, 0, 1, 0, -sinTheta, 0, cosTheta]).reshape((3, 3))
    rm_z = np.array([cosC, -sinC, 0, sinC, cosC, 0, 0, 0, 1]).reshape((3, 3))

    rm_zyx = np.dot(np.dot(rm_z, rm_y), rm_x)

    return rm_zyx

def RM2euler(RM):
    angle_x = np.arctan2(RM[2, 1], RM[2, 2])
    angle_y = np.arctan2(-RM[2, 0], np.sqrt(np.square(RM[2, 1]) + np.square(RM[2, 2])))
    angle_z = np.arctan2(RM[1, 0], RM[0, 0])
    return (angle_x, angle_y, angle_z)