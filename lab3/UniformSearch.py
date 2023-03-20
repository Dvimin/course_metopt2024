import Task as t


class UniformSearchSolver:
    def __init__(self, task: t.Task):
        self.task = task
        self.func_call_count = 0

    def solve(self, eps):
        n = (self.task.b - self.task.a) / eps
        step = (self.task.b - self.task.a) / n
        x_min = self.task.a
        f_min = self.task.func(x_min)
        for i in range(1, int(n+1)):
            x = self.task.a + i * step
            f = self.task.func(x)
            if f < f_min:
                x_min = x
                f_min = f
        return x_min

