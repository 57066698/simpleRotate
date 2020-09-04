# failed

from liegroups.numpy import SO3
import numpy as np
from rotateExample.doubleRotateScene import DoubleRotateScene

rotateScene = DoubleRotateScene()

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    R1 = rotateScene.axis2_1.transform.rotation
    R2 = rotateScene.axis2_2.transform.rotation

    RR_ = np.dot(rotateScene.axis1_1.transform.rotation, rotateScene.axis1_2.transform.rotation)

    P = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
    RRP = np.dot(np.dot(R1, R2), P.transpose()).transpose()
    P_ = np.dot(RR_, P.transpose()).transpose()
    fR = (RRP - P_).reshape(-1)

    J11 = np.identity(3)
    J12 = np.identity(3)
    J13 = np.identity(3)
    J1 = np.concatenate((J11, J12, J13), axis=0)

    J21 = R1
    J22 = R1
    J23 = R1
    J2 = np.concatenate((J21, J22, J23), axis=0)

    res1 = - np.dot(J1.transpose(), fR)
    res2 = - np.dot(J2.transpose(), fR)

    R1 = box_plus(R1, 0.01 * res1)
    R2 = box_plus(R2, 0.01 * res2)

    rotateScene.axis2_1.transform.rotation = R1
    rotateScene.axis2_2.transform.rotation = R2

    # R = SO3.from_matrix(rotation1, normalize=True)
    # P = np.vstack(([1, 1, 0], [0, 1, 0], [0, 0, 1]))
    # P_ = np.dot(rotateScene.axis1.transform.rotation, P.transpose()).transpose()  # [9]
    # RP = np.dot(R.mat, P.transpose()).transpose()  # [9]
    # fR = (RP - P_).reshape(-1)  # [9]-[9] = [9]
    #
    # J1 = -SO3.wedge(RP[0, :])
    # J2 = -SO3.wedge(RP[1, :])
    # J3 = -SO3.wedge(RP[2, :])
    #
    # J = np.concatenate((J1, J2, J3), axis=0)
    # Jt = np.transpose(J)
    # res = - np.dot(Jt, fR)
    #
    # R = box_plus(R, 0.01 * res)
    # rotateScene.axis2.transform.rotation = R.mat


rotateScene.set_convert_func(cal)
rotateScene.start()