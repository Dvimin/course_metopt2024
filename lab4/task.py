import math

import numpy as np


def f(x):
    # return 2 * x[0] ** 2 + x[1] ** 2 + math.cos(6 * x[0] + 5 * x[1]) - x[0] + 2 * x[1]
    return 4 * x[0] + x[1] + 4 * math.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)


def gradf(x):
    return np.asarray([4 + (12 * x[0]) / math.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2),
                       1 + (4 * x[1]) / math.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)])

# return np.asarray(
#    [4 * x[0] - 6 * math.sin(6 * x[0] + 5 * x[1]) - 1, 2 * x[1] - 5 * math.sin(6 * x[0] + 5 * x[1]) + 2])
