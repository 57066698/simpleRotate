from simpleRotate.numpy import euler2RM, RM2euler
import numpy as np

rm = euler2RM(np.array([1, 0, 0]))
print(rm)

euler = RM2euler(rm)
print(euler)