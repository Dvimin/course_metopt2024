import numpy as np

import grad
import grad_dfp

for eps in 0.1, 0.01, 0.001, 0.0001:
    grad.solve(np.array([0, 0]), eps)

for eps in 0.1, 0.01, 0.001, 0.0001:
    grad_dfp.solve(np.array([0,0]), eps)