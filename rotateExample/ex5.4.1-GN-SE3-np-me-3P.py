from simpleRotate.numpy import SO3_numpy, SE3_numpy
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene

rotateScene = SE3Scene()

def get_np_matrix(mat44):
    SE3 = SE3_numpy.normalize(mat44)
    return SE3

P_ori = np.vstack(([1., 0., 0., 1], [0., 1., 0., 1], [0., 0., 1., 1]))
P_ori = np.float32(P_ori)

dtype = np.float32

# @tf.function
def func(SE3_1, SE3_2):

    P = np.matmul(SE3_2, np.transpose(P_ori))  # [4, 3]
    P = np.transpose(P)[:, :3]  # [3, 3]
    P_ = np.matmul(SE3_1, np.transpose(P_ori))  # [4, 3]
    P_ = np.transpose(P_)[:, :3]  # [3, 3]
    diff = np.reshape((P - P_), (-1))

    J1 = - SO3_numpy.wedge(P[0, :])
    J2 = - SO3_numpy.wedge(P[1, :])
    J3 = - SO3_numpy.wedge(P[2, :])

    Jrot = np.concatenate((J1, J2, J3), axis=0)
    Eye = np.eye(3, dtype=dtype)
    Jtrans = np.concatenate((Eye, Eye, Eye), axis=0)
    J = np.concatenate((Jtrans, Jrot), axis=1)

    Jt = np.transpose(J)
    JtJ = np.matmul(Jt, J) + np.eye(6, dtype=dtype) * 1e-8
    res = - np.matmul(Jt, np.expand_dims(diff, axis=1))
    r_ = np.matmul(np.linalg.inv(JtJ), res)
    r_ = np.squeeze(r_, axis=1)

    # print(r_)

    SE3_2_Now = np.matmul(SE3_numpy.exp(r_), SE3_2)
    return SE3_2_Now

def cal():
    SE3_1 = get_np_matrix(rotateScene.axis1.transform.matrix44)
    SE3_2 = get_np_matrix(rotateScene.axis2.transform.matrix44)
    SE3_2_now = func(SE3_1, SE3_2)
    rotateScene.axis2.transform.matrix44 = SE3_2_now

rotateScene.scene.add(cal)
rotateScene.start()