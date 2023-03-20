import Task as t


class GoldenRatioSolver:
    def __init__(self, task: t.Task):
        self.task = task
        self.func_call_count = 0
        self.phi = (1 + 5 ** 0.5) / 2

    def solve(self, eps):
        self.func_call_count = 0
        c = self.task.b - (self.task.b - self.task.a) / self.phi
        d = self.task.a + (self.task.b - self.task.a) / self.phi
        while abs(c - d) > eps:
            if self.task.func(c) < self.task.func(d):
                self.task.b = d
            else:
                self.task.a = c
            self.func_call_count += 2
            c = self.task.b - (self.task.b - self.task.a) / self.phi
            d = self.task.a + (self.task.b - self.task.a) / self.phi
        return (self.task.a + self.task.b) / 2.0

