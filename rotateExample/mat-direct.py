from liegroups.numpy import SO3
import numpy as np
from rotateExample.rotateScene import RotateScene

rotateScene = RotateScene()

speed = 0.1

def close(A, B, C):
    """
    AxB = C calculate B
    :param A:
    :param C:
    :return: B
    """
    return A * (C - np.dot(A, B))

def rm_close():
    C = rotateScene.axis1.transform.rotation
    A = rotateScene.axis2.transform.rotation
    B = np.dot(np.linalg.inv(A), C)

    rotateScene.axis2.transform.rotation = np.dot(A, B)

rotateScene.scene.add(rm_close)