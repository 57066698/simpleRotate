from liegroups.numpy import SO3
import numpy as np

A = SO3.from_rpy(0.1, 0.2, -0.3)
B = SO3.from_rpy(-1.2, 3.4, -0.9)
c = [0.5, -0.3, 1.2]

def box_plus(a, b):
    return SO3.exp(b).dot(a)

def box_minus(a, b):
    return a.dot(SO3.inv(b)).log()

C1 = box_minus(A, B)
C2 = -box_minus(B, A)

print(C1)
print(C2)

print(A)
print(A.inv())