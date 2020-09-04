# part success

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
    R2P = np.dot(R2, P.transpose()).transpose()
    P_ = np.dot(RR_, P.transpose()).transpose()
    fR = (R2P - P_).reshape(-1)

    # J11 = -SO3.wedge(RRP[0, :])
    # J12 = -SO3.wedge(RRP[1, :])
    # J13 = -SO3.wedge(RRP[2, :])
    # J1 = np.concatenate((J11, J12, J13), axis=0)
    # Jt1 = J1.transpose()
    # JtJ1 = np.dot(Jt1, J1) + np.identity(3) * 1e-8
    # res1 = - np.dot(Jt1, fR)
    # r1_ = np.dot(np.linalg.inv(JtJ1), res1)

    J21 = -SO3.wedge(R2P[0, :])
    J22 = -SO3.wedge(R2P[1, :])
    J23 = -SO3.wedge(R2P[2, :])
    J2 = np.concatenate((J21, J22, J23), axis=0)
    Jt2 = J2.transpose()
    JtJ2 = np.dot(Jt2, J2) + np.identity(3) * 1e-8
    res2 = - np.dot(Jt2, fR)
    r2_ = np.dot(np.linalg.inv(JtJ2), res2)

    # R1 = box_plus(R1, r1_)
    R2 = box_plus(R2, r2_)

    # rotateScene.axis2_1.transform.rotation = R1
    rotateScene.axis2_2.transform.rotation = R2


rotateScene.set_convert_func(cal)
rotateScene.start()