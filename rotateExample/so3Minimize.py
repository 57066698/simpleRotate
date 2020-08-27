"""
    Let axis2 follow axis1 by minimize different of up point
    -------------------
    using taylor expansion with SO3 disturb
"""

from liegroups.numpy import SO3
import numpy as np
from rotateExample.rotateScene import RotateScene
from liegroups.numpy import SO3

rotateScene = RotateScene()

def box_minus(SO3_B, SO3_A):
    # diff of B - A
    return SO3.log(SO3.from_matrix(np.dot(SO3_B.mat, np.linalg.inv(SO3_A.mat)), normalize=True))

def box_plus(SO3_A, R3):
    return np.dot(SO3.exp(R3).mat, SO3_A.mat)

def so3_minimize():
    up = [1, 0, 0]
    R_SO3 = SO3.from_matrix(rotateScene.axis2.transform.rotation, normalize=True)
    p_ = np.dot(up, rotateScene.axis1.transform.rotation)
    p = np.dot(up, rotateScene.axis2.transform.rotation)
    # Rp + dR x delta_R - p_ = 0
    # => delta_R = inv(wedge(R x p)) x (Rp - p_)
    wedge = SO3.wedge(p) + np.identity(3) * 1e-8
    delta_R = np.dot((p - p_), np.linalg.inv(wedge))
    R = box_plus(R_SO3, delta_R)
    rotateScene.axis2.transform.rotation = R

rotateScene.scene.add(so3_minimize)
rotateScene.start()