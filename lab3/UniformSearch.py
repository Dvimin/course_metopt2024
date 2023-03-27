import Task as t


class UniformSearchSolver:
    def __init__(self, task: t.Task):
        self.task = task
        self.func_call_count = 0

    def solve(self, eps):
        self.func_call_count = 0
        n = (self.task.b - self.task.a) / eps
        step = (self.task.b - self.task.a) / n
        x, x_max = self.task.a, self.task.a
        f_max = self.task.func(x_max)
        self.func_call_count += 1
        i = 1
        while x <= self.task.b:
            x = self.task.a + i * step
            f = self.task.func(x)
            self.func_call_count += 1
            if f > f_max:
                x_max = x
                f_max = f
            i += 1
        return x_max

