from liegroups.numpy import SO3
import numpy as np
from rotateExample.rotateScene import RotateScene
from liegroups.numpy import SO3

rotateScene = RotateScene()

def box_minus(SO3_B, SO3_A):
    # diff of B - A
    return SO3.log(SO3.from_matrix(np.dot(SO3_B.mat, np.linalg.inv(SO3_A.mat)), normalize=True))

def box_plus(SO3, R3):
    return np.dot(SO3.exp(R3).mat, SO3.mat)

def so3_OneStep():
    SO3_A = SO3.from_matrix(rotateScene.axis1.transform.rotation, normalize=True)
    SO3_B = SO3.from_matrix(rotateScene.axis2.transform.rotation, normalize=True)

    diff = box_minus(SO3_A, SO3_B)
    B = box_plus(SO3_B, diff)
    rotateScene.axis2.transform.rotation = B

rotateScene.scene.add(so3_OneStep)
rotateScene.start()