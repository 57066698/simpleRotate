"""
    提供SE3的各种运算
"""
import numpy as np
from simpleRotate.numpy.SO3_numpy import SO3_numpy

class SE3_numpy:

    @classmethod
    def normalize(cls, matrix):

        trans = matrix[:, 3]
        rotationMatrix = matrix[:3, :3]
        SO3 = SO3_numpy.normalize(rotationMatrix)

        SE3 = np.identity(4, dtype=np.float32)
        SE3[:3, :3] = SO3
        SE3[:, 3] = trans
        return SE3

    @classmethod
    def exp(cls, se3):

        t = se3[:3]
        so3 = se3[3:]
        SO3 = SO3_numpy.exp(so3)

        Vt = np.dot(SO3_numpy.left_jacobi(so3), t)

        mat = np.identity(4, dtype=np.float32)
        mat[:3, :3] = SO3
        mat[:3, 3] = t
        return mat

    @classmethod
    def log(cls, SE3):

        SO3 = SE3[:3, :3]
        so3 = SO3_numpy.log(SO3)
        trans = SE3[:3, 3]

        t = np.dot(SO3_numpy.inv_left_jacobi(so3), trans)
        se3 = np.hstack((t, so3))
        return se3

    @classmethod
    def wedge(cls, xi):

        Xi = np.identity(4, dtype=np.float32)

        Xi[:3, :3] = SO3_numpy.wedge(xi[3:])
        Xi[:, 3] = Xi[:3]

        return Xi

    @classmethod
    def vee(cls, Xi):
        if Xi.shape != (4, 4):
            raise ValueError("shape wrong")
        phi = SO3_numpy.vee(Xi[:3, :3])
        xi_t = Xi[:3, 3]
        xi = np.hstack((xi_t, phi))
        return xi