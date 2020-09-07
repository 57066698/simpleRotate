#

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.oneTwoRotateScene import OneTwoRotateScene
from simple3D import Transform

rotateScene = OneTwoRotateScene()
rotateScene.axis2_1.transform.rotate(Transform.euler2RM([1, 0, 0]))

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation1 = rotateScene.axis2_1.transform.rotation
    rotation2 = rotateScene.axis2_2.transform.rotation
    R1 = SO3.from_matrix(rotation1, normalize=True)
    R2 = SO3.from_matrix(rotation2, normalize=True)
    P = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
    RRP = np.dot(np.dot(R1.mat, R2.mat), P.transpose()).transpose()
    R2P = np.dot(R2.mat, P.transpose()).transpose()
    P_ = np.dot(rotateScene.axis1.transform.rotation, P.transpose()).transpose()
    fR = (RRP - P_).reshape(-1)

    J21 = np.dot(-SO3.wedge(RRP[0, :]), R1.mat)
    J22 = np.dot(-SO3.wedge(RRP[1, :]), R1.mat)
    J23 = np.dot(-SO3.wedge(RRP[2, :]), R1.mat)

    J2 = np.concatenate((J21, J22, J23), axis=0)
    Jt2 = np.transpose(J2)
    JtJ2 = np.dot(Jt2, J2) + np.identity(3) * 1e-8
    res = - np.dot(Jt2, fR)
    r_ = np.dot(np.linalg.inv(JtJ2), res)

    R2 = box_plus(R2, r_)
    rotateScene.axis2_2.transform.rotation = R2.mat


rotateScene.scene.add(cal)
rotateScene.start()