from simpleRotate.numpy.SE3_numpy import SE3_numpy
from simple3D import Transform

A = Transform()
A.rotate(Transform.euler2RM([0.1, 0, 0]))

SE3 = SE3_numpy.normalize(A.matrix44)
print(SE3)

se3 = SE3_numpy.log(SE3)
print(se3)

SE3 = SE3_numpy.exp(se3)
print(SE3)