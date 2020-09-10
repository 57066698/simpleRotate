import tensorflow as tf
import numpy as np
from simple3D import Transform

a = Transform.euler2RM((0.1, 0, 0))

U, S, Vh = np.linalg.svd(a, full_matrices=False)
S_tf, U_tf, V_tf = tf.linalg.svd(a, full_matrices=False)

print(U, U_tf)