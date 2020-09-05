#

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.oneTwoRotateScene import OneTwoRotateScene

rotateScene = OneTwoRotateScene()

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation = rotateScene.axis2_2.transform.rotation
    R = SO3.from_matrix(rotation, normalize=True)
    p = [0, 1, 0]
    p_ = np.dot(rotateScene.axis1.transform.rotation, p)
    Rp = R.dot(p)
    fR = Rp - p_

    J = - SO3.wedge(Rp)
    Jt = np.transpose(J)
    JtJ = np.dot(Jt, J) + np.identity(3) * 1e-8
    res = - np.dot(Jt, fR)
    r_ = np.dot(np.linalg.inv(JtJ), res)

    R = box_plus(R, r_)

    rotateScene.axis2_2.transform.rotation = R.mat

rotateScene.scene.add(cal)
rotateScene.start()
