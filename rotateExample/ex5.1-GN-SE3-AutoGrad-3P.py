from simpleRotate.tf2 import SE3_tf2
from simpleRotate.numpy import SE3_numpy
import numpy as np
from rotateExample.scenes.SE3Scene import SE3Scene
import tensorflow as tf

rotateScene = SE3Scene()

def get_se3_numpy(transform):
    SE3 = SE3_numpy.normalize(transform.matrix44)
    se3 = SE3_numpy.log(SE3)
    return se3

def get_np_matrix(se3_tensor):
    se3_np = se3_tensor.numpy()
    SO3 = SE3_numpy.exp(se3_np)
    return SO3

P_ori = np.vstack(([1., 0., 0., 1.], [0., 1., 0., 1.], [0., 0., 1., 1.]))
P_ori = tf.constant(P_ori, dtype=tf.float32)

@tf.function
def func(axis1_se3, axis2_se3):

    with tf.GradientTape() as g:
        # 1. so3, trans tensors
        Se3_1 = SE3_tf2.exp(axis1_se3)
        Se3_2 = SE3_tf2.exp(axis2_se3)
        # 2. get p, p_
        P = tf.matmul(Se3_2, tf.transpose(P_ori)) # [3, 4]
        P = tf.transpose(P)[:, :3] # [3, 3]
        P_ = tf.matmul(Se3_1, tf.transpose(P_ori)) # [3, 4]
        P_ = tf.transpose(P_)[:, :3] # [3, 3]
        # 3. cal p - p_
        diff = tf.reshape((P - P_), [-1], name="diff_reshape") # [9]

    # 4. get J
    J = g.jacobian(diff, axis2_se3)
    # 5. gauss newton fit J
    Jt = tf.transpose(J)
    JtJ = tf.matmul(Jt, J) + tf.eye(6, dtype=tf.float32) * 1e-9
    Res = - tf.matmul(Jt, tf.expand_dims(diff, axis=1))
    tf.print(J)
    JtJ_inv = tf.linalg.inv(JtJ, name="JtJ_inv")
    theta = tf.matmul(JtJ_inv, Res)
    theta = tf.squeeze(theta, axis=1)
    Se3_2_now = tf.add(axis2_se3, theta)

    return Se3_2_now

axis1_se3 = tf.Variable(np.zeros(6), dtype=tf.float32)
axis2_se3 = tf.Variable(np.zeros(6), dtype=tf.float32)

def cal():
    axis1_se3_np = get_se3_numpy(rotateScene.axis1.transform)
    axis2_se3_np = get_se3_numpy(rotateScene.axis2.transform)
    axis1_se3.assign(axis1_se3_np)
    axis2_se3.assign(axis2_se3_np)
    Se3_2_now = func(axis1_se3, axis2_se3)
    matrix44 = get_np_matrix(Se3_2_now)
    rotateScene.axis2.transform.matrix44 = matrix44

rotateScene.scene.add(cal)
rotateScene.start()