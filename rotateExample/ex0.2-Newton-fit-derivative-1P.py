# failed

from liegroups.numpy import SO3
import numpy as np
from rotateExample.scenes.rotateScene import RotateScene

rotateScene = RotateScene()


def box_plus(a, b):
    return SO3.exp(b).dot(a)


def cal():
    rotation = rotateScene.axis2.transform.rotation
    R = SO3.from_matrix(rotation, normalize=True)
    p = [0, 1, 0]
    p_ = np.dot(rotateScene.axis1.transform.rotation, p)

    We_Rp = SO3.wedge(R.dot(p))
    J = SO3.left_jacobian(R.log())
    dRp_p = SO3.from_matrix(- np.dot(We_Rp, J), normalize=True)
    inv_dRp_p = dRp_p.inv()
    fx = np.dot(R.mat, p) - p_
    # neg_Rp = - np.dot(R.mat, p)
    R_mat = box_plus(R.mat, np.dot(inv_dRp_p.mat, -fx))
    R = SO3.from_matrix(R_mat, normalize=True)

    rotateScene.axis2.transform.rotation = R.mat


rotateScene.scene.add(cal)
rotateScene.start()
