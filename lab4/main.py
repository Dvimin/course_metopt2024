import numpy as np

import grad
import grad_dfp

print(grad.gradsolve(np.array([0, 0]), 0.001))
print(grad_dfp.gradsolve(np.array([0, 0]), 0.001))