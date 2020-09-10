from simpleRotate.numpy import SO3_numpy
from simpleRotate.tf2 import SO3_tf2
from simple3D import Transform
import tensorflow as tf
import numpy as np

a = Transform()
a.rotate(Transform.euler2RM([0.1, 0.5, -1.2]))
a.translate(1, -1, 10)

p = np.array([1, 0, 0, 1])

print(np.matmul(a.matrix44, p))