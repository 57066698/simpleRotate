"""
    final step
    success
"""

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.doubleRotateScene import DoubleRotateScene
from simple3D import Transform

rotateScene = DoubleRotateScene()
# rotateScene.axis2_2.transform.rotate(Transform.euler2RM([1, 0, 0]))

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation1 = rotateScene.axis2_1.transform.rotation
    rotation2 = rotateScene.axis2_2.transform.rotation
    R1 = SO3.from_matrix(rotation1, normalize=True)
    R2 = SO3.from_matrix(rotation2, normalize=True)

    rotation1_ = rotateScene.axis1_1.transform.rotation
    rotation2_ = rotateScene.axis1_2.transform.rotation

    R1_ = SO3.from_matrix(rotation1_, normalize=True)
    R2_ = SO3.from_matrix(rotation2_, normalize=True)

    P = np.array([0., 1., 0.])
    RRP = np.dot(np.dot(R1.mat, R2.mat), P)
    P_ = np.dot(np.dot(R1_.mat, R2_.mat), P)
    fR = (RRP - P_)

    J1 = -SO3.wedge(RRP)
    J2 = np.dot(-SO3.wedge(RRP), R1.mat)

    J = np.hstack([J1, J2])

    Jt = np.transpose(J)
    res = - np.dot(Jt, fR)
    r = 0.01 * res

    r1 = r[:3]
    r2 = r[3:6]

    R1 = box_plus(R1, r1)
    R2 = box_plus(R2, r2)

    rotateScene.axis2_1.transform.rotation = R1.mat
    rotateScene.axis2_2.transform.rotation = R2.mat

rotateScene.scene.add(cal)
rotateScene.start()