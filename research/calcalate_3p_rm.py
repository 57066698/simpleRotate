import numpy as np
from simpleRotate.numpy import euler2RM, RM2euler

R = euler2RM([0.5, 0, 0])

p1 = np.array([1, 0, 0])
p2 = np.array([0, 1, 0])
p3 = np.array([0, 0, 1])

p1_ = np.dot(R, p1)
p2_ = np.dot(R, p2)
p3_ = np.dot(R, p3)

P = np.stack([p1, p2, p3], axis=1)
P_ = np.stack([p1_, p2_, p3_], axis=1)

print(P)
print(P_)

R = np.zeros((3, 3))
R = np.dot(P_, np.linalg.inv(P))

print(RM2euler(R))