import math

import numpy as np


def f(x):
    return 5 * x[0] + x[1] + 4 * math.sqrt(1 + x[0] ** 2 + 3 * x[1] ** 2)


def gradf(x):
    return np.array([5 + (4 * x[0]) / math.sqrt(1 + x[0] ** 2 + 3 * x[1] ** 2),
                    1 + (12 * x[1]) / math.sqrt(1 + x[0] ** 2 + 3 * x[1] ** 2)])
