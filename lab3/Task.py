from numpy import sqrt


class Task:
    def __init__(self):
        self.a = 0.2
        self.b = 1.0
        self.x_max = 0.562

    def func(self, x):
        return x * sqrt(1.0 - x) / (1.0 + x)
