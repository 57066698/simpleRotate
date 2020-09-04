from liegroups.numpy import SO3
import numpy as np
from rotateExample.rotateScene import RotateScene

rotateScene = RotateScene()

def rm_to_SO3():
    rm = rotateScene.axis1.transform.rotation
    rm_SO3 = SO3.from_matrix(rm, normalize=True)
    rotateScene.axis2.transform.rotation = rm_SO3.mat

rotateScene.scene.add(rm_to_SO3)