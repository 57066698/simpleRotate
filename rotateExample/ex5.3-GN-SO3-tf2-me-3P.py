from simpleRotate.tf2 import SO3_tf2
from simpleRotate.numpy import SO3_numpy
from simple3D import Transform
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene
import tensorflow as tf

rotateScene = SE3Scene()
rotateScene.axis1.transform.rotate(Transform.euler2RM((1, 0, 0)))

def get_np_matrix(rotation):
    SO3 = SO3_numpy.normalize(rotation)
    return SO3

P_ori = np.vstack(([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]))
P_ori = tf.constant(P_ori, dtype=tf.float32)

# @tf.function
def func(SO3_1, SO3_2):
    # 1. so3, trans tensors
    # 2. get p, p_
    P = tf.matmul(SO3_2, tf.transpose(P_ori)) # [4, 3]
    P = tf.transpose(P)[:, :3] # [3, 3]
    P_ = tf.matmul(SO3_1, tf.transpose(P_ori)) # [4, 3]
    P_ = tf.transpose(P_)[:, :3] # [3, 3]
    # 3. cal p - p_
    diff = tf.reshape((P - P_), [-1], name="diff_reshape") # [9]
    # 4. get J
    J1 = -SO3_tf2.wedge(P[0, :])
    J2 = -SO3_tf2.wedge(P[1, :])
    J3 = -SO3_tf2.wedge(P[2, :])

    J = tf.concat((J1, J2, J3), axis=0)

    # 5. gauss newton fit J
    Jt = tf.transpose(J)
    JtJ = tf.matmul(Jt, J) + tf.eye(3, dtype=tf.float32) * 1e-9
    Res = - tf.matmul(Jt, tf.expand_dims(diff, axis=1))
    JtJ_inv = tf.linalg.inv(JtJ, name="JtJ_inv")
    theta = tf.matmul(JtJ_inv, Res)
    theta = tf.squeeze(theta, axis=1)
    SO3_2_now = tf.matmul(SO3_tf2.exp(theta), SO3_2)

    return SO3_2_now

axis1_rotation = tf.Variable(np.zeros((3, 3)), dtype=tf.float32)
axis2_rotation = tf.Variable(np.zeros((3, 3)), dtype=tf.float32)

def cal():
    SO3_1 = get_np_matrix(rotateScene.axis1.transform.rotation)
    SO3_2 = get_np_matrix(rotateScene.axis2.transform.rotation)
    axis1_rotation.assign(SO3_1)
    axis2_rotation.assign(SO3_2)
    SO3_2_now = func(axis1_rotation, axis2_rotation)
    rotateScene.axis2.transform.rotation = SO3_2_now.numpy()

rotateScene.scene.add(cal)
rotateScene.start()