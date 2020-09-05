# successed

import numpy as np
from rotateExample.scenes.rotateScene import RotateScene

rotateScene = RotateScene()

def cal():
    rotation = rotateScene.axis1.transform.rotation

    p1 = [1, 0, 0]
    p2 = [0, 1, 0]
    p3 = [0, 0, 1]
    P = np.stack([p1, p2, p3], axis=1)

    p1_ = np.dot(rotation, [1, 0, 0])
    p2_ = np.dot(rotation, [0, 1, 0])
    p3_ = np.dot(rotation, [0, 0, 1])
    P_ = np.stack([p1_, p2_, p3_], axis=1)

    R = np.dot(P_, np.linalg.inv(P))

    rotateScene.axis2.transform.rotation = R

rotateScene.scene.add(cal)
rotateScene.start()