"""
    提供SO3的各种运算
"""
import tensorflow as tf
from .Dtype import dtype

class SO3_tf2:

    @classmethod
    def normalize(cls, rotationMatrix):
        _, U, V = tf.linalg.svd(rotationMatrix, full_matrices=False)

        S = tf.constant([[0, 1, 0], [0, 0, 0], [0, 1, 0]], dtype=dtype) + tf.constant([[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                      dtype=dtype) * (tf.linalg.det(U) * tf.linalg.det(V))

        return tf.matmul(tf.matmul(U, S), tf.transpose(V))

    @classmethod
    def exp(cls, so3):
        angle = tf.linalg.norm(so3)
        if angle <= 1e-5:
            return tf.eye(3, dtype=dtype) + SO3_tf2.wedge(so3)

        axis = so3 / angle # normalized
        sin = tf.sin(angle)
        cos = tf.cos(angle)

        return cos * tf.eye(3, dtype=dtype) + (1-cos) * tf.tensordot(axis, axis, axes=0) + sin * SO3_tf2.wedge(axis)

    @classmethod
    def wedge(cls, phi):

        inds = tf.constant([1, 2, 3, 5, 6, 7], dtype=tf.int32)
        inds = tf.expand_dims(inds, axis=1)
        updates = tf.stack([-phi[2], phi[1], phi[2], -phi[0], -phi[1], phi[0]])
        Phi = tf.scatter_nd(inds, updates, [9])
        Phi = tf.reshape(Phi, (3, 3))

        return Phi

    @classmethod
    def log(cls, SO3):
        cos_angle = tf.clip_by_value(0.5 * tf.linalg.trace(SO3) - 0.5, -1., 1)
        angle = tf.math.acos(cos_angle)

        # use taylor first-order to handler SO3
        if angle <= 1e-5:
            return SO3_tf2.vee(SO3 - tf.eye(3, dtype=dtype))

        return SO3_tf2.vee((0.5 * angle / tf.sin(angle)) * (SO3 - tf.transpose(SO3)))

    @classmethod
    def vee(cls, Phi):
        if Phi.shape != (3, 3):
            raise ValueError("shape wrong")
        phi = tf.stack([Phi[2, 1], Phi[0, 2], Phi[1, 0]])
        return phi

    @classmethod
    def left_jacobi(cls, so3):
        angle = tf.linalg.norm(so3)

        if angle < 1e-5:
            return tf.eye(3, dtype=dtype) + 0.5 * cls.wedge(so3)

        axis = so3 / angle  # normalized
        sin = tf.sin(angle)
        cos = tf.cos(angle)

        J = (sin / angle) * tf.eye(3, dtype=dtype) + ((1 - sin) / angle) * tf.tensordot(axis, axis, axes=0) + (
                    (1 - cos) / angle) * SO3_tf2.wedge(so3)
        return J

    @classmethod
    def inv_left_jacobi(cls, so3):
        angle = tf.linalg.norm(so3)

        if angle <= 1e-5:
            return tf.eye(3, dtype=dtype) - 0.5 * cls.wedge(so3)

        axis = so3 / angle  # normalized
        half_angle = 0.5 * angle
        cot_half_angle = 1. / tf.math.tan(half_angle)

        return half_angle * cot_half_angle * tf.eye(3, dtype=dtype) + \
               (1 - half_angle * cot_half_angle) * tf.tensordot(axis, axis, axes=0) - \
               half_angle * SO3_tf2.wedge(axis)