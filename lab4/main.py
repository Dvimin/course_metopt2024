import numpy as np

import grad
import grad_dfp

print(f'Заданная точность = {0.01}')
x, y, solution, iters = grad.solve(np.array([0, 0]), 0.01)
#print(x, y)

"""
for eps in 0.1, 0.01, 0.001, 0.0001:
    print(f'Заданная точность = {eps}')
    x, y, solution, iters = grad_dfp.solve(np.array([0,0]), eps)
    print(x, y)"""