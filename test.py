import numpy as np
import time

A = np.random.rand(400, 400)
time1 = time.time()
B = np.linalg.inv(A)
time2 = time.time()

print(time2 - time1)