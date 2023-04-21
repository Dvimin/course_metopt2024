import numpy as np
import task as t
import pivoter as p
import ort_checker as ort


def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)


def solve(x_init, eps): # выбрали эпсилон
    x = []
    y = []
    x_k = x_init
    x.append(x_k[0])
    y.append(x_k[1])
    k = 0
    grad = t.gradf(x_k) # вычисляем градиент
    m = 4
    M = 12
    while norm(grad) > eps:
        a_k = p.secondary_point(x_k, grad, eps) # решаем задачу одномерной минимизации
        x_k = x_k - a_k * grad
        x.append(x_k[0])
        y.append(x_k[1])
        grad = t.gradf(x_k)
        k += 1
        print(k)
        print(f"||grad f(x_k)||^2 = {norm(t.gradf(x_k))**2:.4f}")
        print(f"||grad f(x_k)|| = {norm(t.gradf(x_k)):.2f}")
        print(f'{m}*(1+ {m}/{M})*[{t.f(x_k):.2f} - 3.11] = {m*(1+m/M)*(t.f(x_k)-3.11):.4f}')

    return x, y, x_k, k
