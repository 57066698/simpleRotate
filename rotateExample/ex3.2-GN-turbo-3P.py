#

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.oneTwoRotateScene import OneTwoRotateScene

rotateScene = OneTwoRotateScene()

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation = rotateScene.axis2_2.transform.rotation
    R2 = SO3.from_matrix(rotation, normalize=True)
    P = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
    R2P = np.dot(R2.mat, P.transpose()).transpose()
    P_ = np.dot(rotateScene.axis1.transform.rotation, P.transpose()).transpose()
    fR = (R2P - P_).reshape(-1)

    J21 = -SO3.wedge(R2P[0, :])
    J22 = -SO3.wedge(R2P[1, :])
    J23 = -SO3.wedge(R2P[2, :])

    J2 = np.concatenate((J21, J22, J23), axis=0)
    Jt2 = np.transpose(J2)
    JtJ2 = np.dot(Jt2, J2) + np.identity(3) * 1e-8
    res = - np.dot(Jt2, fR)
    r_ = np.dot(np.linalg.inv(JtJ2), res)

    R2 = box_plus(R2, r_)

    rotateScene.axis2_2.transform.rotation = R2.mat

rotateScene.scene.add(cal)
rotateScene.start()
