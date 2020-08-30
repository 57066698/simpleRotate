import numpy as np

R = np.zeros((3, 3))
p = np.array([0, 1, 0])
p_ = np.array([1, 0, 0])

# newton:
# (R+r)p - p_ = 0
# Rp + dRp/dp * r - p = 0
#

def newton():
    Rp = np.dot(R, p)
    res = Rp - p
    # 因为px,pz为0
    R[0, 1] = p_[0]/p[1]
    R[1, 1] = p_[1]/p[1]
    R[2, 1] = p_[2]/p[1]
    return R

r = newton()
print(r)
print(np.dot(r, p))
