#

from liegroups.numpy import SO3
import numpy as np
from rotateExample.rotateScene import RotateScene

rotateScene = RotateScene()

def cal():
    rotation = rotateScene.axis2.transform.rotation

    RM_SO3 = SO3.from_matrix(rotation)



    rotateScene.axis2.transform.rotation = R

rotateScene.scene.add(cal)
rotateScene.start()