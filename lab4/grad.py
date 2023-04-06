import numpy as np

import task as t
import pivoter as p

def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)


def gradsolve(x_init, eps):
    x_k = x_init
    k = 0
    grad = t.gradf(x_k)
    a_k = 0.95
    while norm(grad) > eps:
        x_k = x_k - a_k * grad
        a_k = p.golden_ratio(x_k, eps)
        grad = t.gradf(x_k)
        k += 1
    return x_k
