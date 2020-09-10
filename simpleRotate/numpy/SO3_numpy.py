"""
    提供SO3的各种运算
"""
import numpy as np

class SO3_numpy:

    @classmethod
    def normalize(cls, rotationMatrix):
        U, S, Vh = np.linalg.svd(rotationMatrix, full_matrices=False)
        S = np.identity(3)
        S[2, 2] = np.linalg.det(U) * np.linalg.det(Vh)
        return U.dot(S).dot(Vh)

    @classmethod
    def exp(cls, so3):
        angle = np.linalg.norm(so3)
        if np.isclose(angle, 0.):
            return np.identity(3) + SO3_numpy.wedge(so3)

        axis = so3 / angle # normalized
        sin = np.sin(angle)
        cos = np.cos(angle)

        return cos * np.identity(3) + (1-cos) * np.outer(axis, axis) + sin * SO3_numpy.wedge(axis)

    @classmethod
    def wedge(cls, phi):
        Phi = np.zeros((3, 3))
        Phi[0, 1] = -phi[2]
        Phi[1, 0] = phi[2]
        Phi[0, 2] = phi[1]
        Phi[2, 0] = -phi[1]
        Phi[1, 2] = -phi[0]
        Phi[2, 1] = phi[0]
        return Phi

    @classmethod
    def log(cls, SO3):
        cos_angle = np.clip(0.5 * np.trace(SO3) - 0.5, -1., 1)
        angle = np.arccos(cos_angle)

        # use taylor first-order to handler SO3
        if np.isclose(angle, 0.):
            return SO3_numpy.vee(SO3 - np.identity(3))

        return SO3_numpy.vee((0.5 * angle / np.sin(angle)) * (SO3 - np.transpose(SO3)))

    @classmethod
    def vee(cls, Phi):
        if Phi.shape != (3, 3):
            raise ValueError("shape wrong")
        phi = np.empty(3)
        phi[0] = Phi[2, 1]
        phi[1] = Phi[0, 2]
        phi[2] = Phi[1, 0]
        return phi

    @classmethod
    def left_jacobi(cls, so3):
        angle = np.linalg.norm(so3)
        axis = so3 / angle  # normalized
        sin = np.sin(angle)
        cos = np.cos(angle)

        if np.isclose(angle, 0.):
            return np.identity(3) + 0.5 * cls.wedge(so3)

        J = (sin / angle) * np.identity(3) + ((1 - sin) / angle) * np.outer(axis, axis) + (
                    (1 - cos) / angle) * SO3_numpy.wedge(so3)
        return J

    @classmethod
    def inv_left_jacobi(cls, so3):
        angle = np.linalg.norm(so3)
        axis = so3 / angle  # normalized

        if np.isclose(angle, 0.):
            return np.identity(3) - 0.5 * cls.wedge(so3)

        half_angle = 0.5 * angle
        cot_half_angle = 1. / np.tan(half_angle)

        return half_angle * cot_half_angle * np.identity(3) + \
               (1 - half_angle * cot_half_angle) * np.outer(axis, axis) - \
               half_angle * SO3_numpy.wedge(axis)