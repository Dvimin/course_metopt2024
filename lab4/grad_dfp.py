import numpy as np

import task as t
import pivoter as p
import ort_checker as ort

def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)

def refresh_matrix(A, x_0, x_1):
    dx = x_1 - x_0
    dw = t.gradf(x_0) - t.gradf(x_1)
    return A - np.outer(dx, dx) / np.dot(dw, dx) - A.dot(np.outer(dw, dw)).dot(A.transpose()) / (
        np.dot(dw, A.dot(dw)))

def solve(x_init, eps):
    x = []
    y = []
    x_0 = x_init
    x_k = x_init

    x.append(x_k[0])
    y.append(x_k[1])

    k = 0
    grad = t.gradf(x_0)
    A = np.eye(2)
    while norm(grad) >= eps:
        po = A.dot(grad)
        alpha = p.secondary_point(x_0, po, eps)
        x_0 = x_k
        x_k = x_k - alpha * po

        x.append(x_k[0])
        y.append(x_k[1])

        grad = t.gradf(x_k)
        k += 1
        if k % 2 == 0:
            A = refresh_matrix(A, x_0, x_k)


    return x, y, x_k, k
