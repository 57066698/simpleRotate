from simpleRotate.tf2 import SO3_tf2, SE3_tf2
import tensorflow as tf

se3 = tf.constant([0, 0, 0, 0.1, 0, 0], dtype=tf.float32)
SE3 = SE3_tf2.exp(se3)
print(SE3)
se3 = SE3_tf2.log(SE3)
print(se3)