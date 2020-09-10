"""
    提供SE3的各种运算
"""
import tensorflow as tf
from simpleRotate.tf2.SO3_tf2 import SO3_tf2
from .Dtype import dtype

class SE3_tf2:

    @classmethod
    def normalize(cls, matrix):

        trans = matrix[:, 3]
        rotationMatrix = matrix[:3, :3]
        SO3 = SO3_tf2.normalize(rotationMatrix)

        SE3 = tf.eye(4, dtype=dtype)
        SE3[:3, :3] = SO3
        SE3[:, 3] = trans
        return SE3

    @classmethod
    def exp(cls, se3):

        t = se3[:3]
        so3 = se3[3:]
        SO3 = SO3_tf2.exp(so3)

        # Vt = tf.matmul(SO3_tf2.left_jacobi(so3), tf.expand_dims(t, axis=1))

        mat = tf.concat((SO3, tf.expand_dims(t, axis=1)), axis=1)
        mat = tf.concat((mat, tf.constant([[0, 0, 0, 1]], dtype=dtype)), axis=0)

        return mat

    @classmethod
    def log(cls, SE3):

        SO3 = SE3[:3, :3]
        so3 = SO3_tf2.log(SO3)
        trans = SE3[:3, 3]

        t = tf.matmul(SO3_tf2.inv_left_jacobi(so3), tf.expand_dims(trans, axis=1))
        t = tf.squeeze(t, axis=1)
        se3 = tf.concat((t, so3), axis=0)
        return se3

    # @classmethod
    # def wedge(cls, xi):
    #
    #     Xi = tf.eye(4, dtype=dtype)
    #
    #     Xi[:3, :3] = SO3_mat.wedge(xi[3:])
    #     Xi[:, 3] = Xi[:3]
    #
    #     return Xi
    #
    # @classmethod
    # def vee(cls, Xi):
    #     if Xi.shape != (4, 4):
    #         raise ValueError("shape wrong")
    #     phi = SO3_mat.vee(Xi[:3, :3])
    #     xi_t = Xi[:3, 3]
    #     xi = np.hstack((xi_t, phi))
    #     return xi