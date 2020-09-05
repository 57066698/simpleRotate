# success

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.rotateScene import RotateScene

rotateScene = RotateScene()

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation = rotateScene.axis2.transform.rotation

    R = SO3.from_matrix(rotation, normalize=True)
    P = np.vstack(([1, 1, 0], [0, 1, 0], [0, 0, 1]))
    P_ = np.dot(rotateScene.axis1.transform.rotation, P.transpose()).transpose() # [9]
    RP = np.dot(R.mat, P.transpose()).transpose() # [9]
    fR = (RP - P_).reshape(-1) # [9]-[9] = [9]

    J1 = -SO3.wedge(RP[0, :])
    J2 = -SO3.wedge(RP[1, :])
    J3 = -SO3.wedge(RP[2, :])

    J = np.concatenate((J1, J2, J3), axis=0)
    Jt = np.transpose(J)
    JtJ = np.dot(Jt, J) + np.identity(3) * 1e-8
    res = - np.dot(Jt, fR)
    r_ = np.dot(np.linalg.inv(JtJ), res)

    R = box_plus(R, r_)

    rotateScene.axis2.transform.rotation = R.mat

rotateScene.scene.add(cal)
rotateScene.start()