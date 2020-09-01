# half successed, only works on positive y

from liegroups.numpy import SO3
import numpy as np
from rotateExample.rotateScene import RotateScene

rotateScene = RotateScene()


def box_plus(a, b):
    return SO3.exp(b).dot(a)

def cal():
    rotation = rotateScene.axis2.transform.rotation
    R = SO3.from_matrix(rotation, normalize=True)
    p = [0, 1, 0]
    p_ = np.dot(rotateScene.axis1.transform.rotation, p)

    We_Rp = SO3.wedge(R.dot(p))
    dRp_p = SO3.from_matrix(-We_Rp, normalize=True)
    inv_dRp_p = dRp_p.inv()
    fx = R.dot(p) - p_
    x0 = R.mat
    x = box_plus(x0, np.dot(inv_dRp_p.mat, -fx))
    R = SO3.from_matrix(x, normalize=True)

    rotateScene.axis2.transform.rotation = R.mat


rotateScene.scene.add(cal)
rotateScene.start()
