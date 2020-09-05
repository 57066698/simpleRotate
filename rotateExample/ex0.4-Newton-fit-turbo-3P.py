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
    P = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
    manifold = np.array([0., 0., 0.])

    for i in range(3):
        p_ = np.dot(rotateScene.axis1.transform.rotation, P[i])

        We_Rp = SO3.wedge(R.dot(p_))
        dRp_p = SO3.from_matrix(-We_Rp, normalize=True)
        inv_dRp_p = dRp_p.inv()
        fx = R.dot(P[i]) - p_

        manifold += np.dot(inv_dRp_p.mat, -fx)

    x0 = R.mat
    manifold = manifold / 3
    x = box_plus(x0, manifold)
    R = SO3.from_matrix(x, normalize=True)

    rotateScene.axis2.transform.rotation = R.mat

rotateScene.scene.add(cal)
rotateScene.start()
