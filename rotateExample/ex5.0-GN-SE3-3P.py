#

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene

rotateScene = SE3Scene()

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation = rotateScene.axis2.transform.rotation
    R2 = SO3.from_matrix(rotation, normalize=True)
    P = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
    R2P = np.dot(R2.mat, P.transpose()).transpose()
    P_ = np.dot(rotateScene.axis1.transform.rotation, P.transpose()).transpose()
    fR = (R2P - P_).reshape(-1)

    J1 = -SO3.wedge(R2P[0, :])
    J2 = -SO3.wedge(R2P[1, :])
    J3 = -SO3.wedge(R2P[2, :])

    J4 = np.array([-1.0, 0, 0])
    J5 = np.array([.0, -1.0, 0])
    J6 = np.array([.0, .0, -1])

    J = np.concatenate((J1, J2, J3, J4, J5, J6), axis=0)
    Jt = np.transpose(J)
    JtJ = np.dot(Jt, J2) + np.identity(3) * 1e-8
    res = - np.dot(Jt, fR)
    r_ = np.dot(np.linalg.inv(JtJ), res)

    r_rotate = r_[:3]
    r_translate = r_[3:6]
    R2 = box_plus(R2, r_rotate)

    rotateScene.axis2.transform.rotation = R2.mat
    rotateScene.axis2.transform.pos += r_translate

rotateScene.scene.add(cal)
rotateScene.start()
