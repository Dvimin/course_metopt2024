import numpy as np

#if k > 2:
#    (ort.is_orthogonal(np.asarray([x[-3], y[-3]]), np.asarray([x[-2], y[-2]]), np.asarray([x[-1], y[-1]])))

def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)

def is_orthogonal(x_1, x_2, x_3):
    dx1 = x_2 - x_1
    dx1 = dx1/norm(dx1)
    dx2 = x_3 - x_2
    dx2 = dx2/norm(dx2)
    print(dx1[0]*dx2[0] + dx1[1]*dx2[1])
    return