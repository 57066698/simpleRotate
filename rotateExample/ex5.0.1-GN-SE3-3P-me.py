from simpleRotate.numpy import SO3_numpy
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene

rotateScene = SE3Scene()

def box_plus(a, b):
    return np.dot(SO3_numpy.exp(b), a)

def cal():
    rotation = rotateScene.axis2.transform.rotation
    trans = rotateScene.axis2.transform.pos
    R2 = SO3_numpy.normalize(rotation)
    P = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
    R2P = np.dot(R2, P.transpose()).transpose() + trans
    P_ = np.dot(rotateScene.axis1.transform.rotation, P.transpose()).transpose() + rotateScene.axis1.transform.pos
    fR = (R2P - P_).reshape(-1)

    J1 = -SO3_numpy.wedge(R2P[0, :])
    J2 = -SO3_numpy.wedge(R2P[1, :])
    J3 = -SO3_numpy.wedge(R2P[2, :])

    J = np.zeros((9, 6))
    J[:, :3] = np.concatenate((J1, J2, J3), axis=0)
    J[:, 3:6] = np.concatenate((np.identity(3), np.identity(3), np.identity(3)), axis=0)
    Jt = np.transpose(J)
    JtJ = np.dot(Jt, J) + np.identity(6) * 1e-8
    res = - np.dot(Jt, fR)
    r_ = np.dot(np.linalg.inv(JtJ), res)

    r_rotate = r_[:3]
    r_translate = r_[3:6]
    R2 = box_plus(R2, r_rotate)

    rotateScene.axis2.transform.rotation = R2
    rotateScene.axis2.transform.pos += r_translate

rotateScene.scene.add(cal)
rotateScene.start()
