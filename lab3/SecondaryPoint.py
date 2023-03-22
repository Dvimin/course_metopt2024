import Task as t


class SecondaryPointSolver:
    def __init__(self, task: t.Task):
        self.task = task
        self.func_call_count = 0

    def solve(self, eps):
        self.func_call_count = 0
        a = self.task.a
        b = self.task.b
        while abs(b - a) >= eps:
            c = a + (b - a) / 3
            d = b - (b - a) / 3
            self.func_call_count += 2
            if self.task.func(c) < self.task.func(d):
                b = d
            else:
                a = c
        return (a + b) / 2.0

