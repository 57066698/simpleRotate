from simpleRotate.tf2 import SE3_tf2, SO3_tf2
from simpleRotate.numpy import SE3_numpy
from simple3D import Transform
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene
import tensorflow as tf

rotateScene = SE3Scene()
rotateScene.axis1.transform.rotate(Transform.euler2RM((1, 0, 0)))

def get_se3_numpy(transform):
    SE3 = SE3_numpy.normalize(transform.matrix44)
    se3 = SE3_numpy.log(SE3)
    return se3

def get_np_matrix(SE3_tensor):
    SE3 = SE3_tensor.numpy()
    return SE3

P_ori = np.vstack(([1., 0., 0., 1.], [0., 1., 0., 1.], [0., 0., 1., 1.]))
P_ori = tf.constant(P_ori, dtype=tf.float32)

# @tf.function
def func(axis1_se3, axis2_se3):

    # 1. so3, trans tensors
    Se3_1 = SE3_tf2.exp(axis1_se3)
    Se3_2 = SE3_tf2.exp(axis2_se3)
    # 2. get p, p_
    P = tf.matmul(Se3_2, tf.transpose(P_ori)) # [4, 3]
    P = tf.transpose(P)[:, :3] # [3, 3]
    P_ = tf.matmul(Se3_1, tf.transpose(P_ori)) # [4, 3]
    P_ = tf.transpose(P_)[:, :3] # [3, 3]
    # 3. cal p - p_
    diff = tf.reshape((P - P_), [-1], name="diff_reshape") # [9]
    # 4. get J
    J1 = -SO3_tf2.wedge(P[0, :])
    J2 = -SO3_tf2.wedge(P[1, :])
    J3 = -SO3_tf2.wedge(P[2, :])

    Jrot = tf.concat((J1, J2, J3), axis=0)
    Jid = tf.concat((tf.eye(3, dtype=tf.float32), tf.eye(3, dtype=tf.float32), tf.eye(3, dtype=tf.float32)), axis=0)
    J = tf.concat((Jid, Jrot), axis=1)
    tf.print(J)

    # 5. gauss newton fit J
    Jt = tf.transpose(J)
    JtJ = tf.matmul(Jt, J) + tf.eye(6, dtype=tf.float32) * 1e-9
    Res = - tf.matmul(Jt, tf.expand_dims(diff, axis=1))
    JtJ_inv = tf.linalg.inv(JtJ, name="JtJ_inv")
    theta = tf.matmul(JtJ_inv, Res)
    theta = tf.squeeze(theta, axis=1)
    Se3_2_now = tf.matmul(SE3_tf2.exp(theta), Se3_2)

    return Se3_2_now

axis1_se3 = tf.Variable(np.zeros(6), dtype=tf.float32)
axis2_se3 = tf.Variable(np.zeros(6), dtype=tf.float32)

def cal():
    axis1_se3_np = get_se3_numpy(rotateScene.axis1.transform)
    axis2_se3_np = get_se3_numpy(rotateScene.axis2.transform)
    axis1_se3.assign(axis1_se3_np)
    axis2_se3.assign(axis2_se3_np)
    Se3_2_now = func(axis1_se3, axis2_se3)
    print(Se3_2_now)
    matrix44 = get_np_matrix(Se3_2_now)
    rotateScene.axis2.transform.matrix44 = matrix44

rotateScene.scene.add(cal)
rotateScene.start()