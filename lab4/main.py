import numpy as np

import grad
import grad_dfp

print(grad.solve(np.array([0, 0]), 0.001))
print(grad_dfp.solve(np.array([0, 0]), 0.001))