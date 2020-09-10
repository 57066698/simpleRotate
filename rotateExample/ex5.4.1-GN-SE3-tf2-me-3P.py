from simpleRotate.numpy import SO3_numpy, SE3_numpy
from simpleRotate.tf2 import SO3_tf2, SE3_tf2
import tensorflow as tf
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene

rotateScene = SE3Scene()

def get_np_matrix(mat44):
    SE3 = SE3_numpy.normalize(mat44)
    return SE3

P_ori = np.vstack(([1., 0., 0., 1], [0., 1., 0., 1], [0., 0., 1., 1]))
P_ori = tf.constant(P_ori, dtype=tf.float32)

dtype = tf.float32

# @tf.function
def func(SE3_1, SE3_2):

    P = tf.matmul(SE3_2, tf.transpose(P_ori))  # [4, 3]
    P = tf.transpose(P)[:, :3]  # [3, 3]
    P_ = tf.matmul(SE3_1, tf.transpose(P_ori))  # [4, 3]
    P_ = tf.transpose(P_)[:, :3]  # [3, 3]
    diff = tf.reshape((P - P_), (-1), name="diff_reshape")

    J1 = - SO3_tf2.wedge(P[0, :])
    J2 = - SO3_tf2.wedge(P[1, :])
    J3 = - SO3_tf2.wedge(P[2, :])

    Jrot = tf.concat((J1, J2, J3), axis=0)
    Eye = tf.eye(3, dtype=tf.float32)
    Jtrans = tf.concat((Eye, Eye, Eye), axis=0)
    J = tf.concat((Jtrans, Jrot), axis=1)

    Jt = tf.transpose(J)
    JtJ = tf.matmul(Jt, J) + tf.eye(6, dtype=dtype) * 1e-8
    res = - tf.matmul(Jt, tf.expand_dims(diff, axis=1))
    r_ = tf.matmul(tf.linalg.inv(JtJ), res)
    r_ = tf.squeeze(r_, axis=1)

    SE3_2_Now = tf.matmul(SE3_tf2.exp(r_), SE3_2)
    return SE3_2_Now

axis1_matrix = tf.Variable(np.zeros((4, 4)), dtype=tf.float32)
axis2_matrix = tf.Variable(np.zeros((4, 4)), dtype=tf.float32)

def cal():
    SE3_1 = get_np_matrix(rotateScene.axis1.transform.matrix44)
    SE3_2 = get_np_matrix(rotateScene.axis2.transform.matrix44)
    axis1_matrix.assign(SE3_1)
    axis2_matrix.assign(SE3_2)
    SE3_2_now = func(axis1_matrix, axis2_matrix)
    rotateScene.axis2.transform.matrix44 = SE3_2_now.numpy()

rotateScene.scene.add(cal)
rotateScene.start()
