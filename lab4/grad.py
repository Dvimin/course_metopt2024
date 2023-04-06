import numpy as np

import task as t
import pivoter as p


def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)


def solve(x_init, eps):
    x = []
    y = []
    x_k = x_init
    x.append(x_k[0])
    y.append(x_k[1])
    k = 0
    grad = t.gradf(x_k)
    while norm(grad) > eps:
        a_k = p.golden_ratio(x_k, grad, eps)
        x_k = x_k - a_k * grad
        x.append(x_k[0])
        y.append(x_k[1])
        grad = t.gradf(x_k)
        k += 1
    return x, y, x_k, k
