# part success

from liegroups.numpy import SO3
import numpy as np
from rotateExample.NRotateScene import NRotateScene

rotateScene = NRotateScene(4)

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def get_J(i):
    assert i>0
    R1 = rotateScene.axises2[0].transform.rotation
    R2 = rotateScene.axises2[i].transform.rotation

    P = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
    RRP = np.dot(np.dot(R1, R2), P.transpose()).transpose()
    RR_ = rotateScene.axises1[i].transform.world_rotation
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

    return J1, J2, fR

def cal():

    J1_list = []
    fR_list = []

    for i in range(1, rotateScene.n):
        J1, J2, fR = get_J(i)
        res2 = - np.dot(J2.transpose(), fR)
        R2 = rotateScene.axises2[i].transform.rotation
        R2 = box_plus(R2, 0.01 * res2)

        rotateScene.axises2[i].transform.rotation = R2

        J1_list.append(J1)
        fR_list.append(fR)

    J1 = np.array(J1_list).reshape((3, -1 ))



    rotateScene.axis2_1.transform.rotation = R1
    rotateScene.axis2_2.transform.rotation = R2


rotateScene.set_convert_func(cal)
rotateScene.start()