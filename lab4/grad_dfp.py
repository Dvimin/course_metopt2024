import numpy as np

import task

class gdfp:
    t = task.Task()

    def refresh_matrix(self, A):
        dx = self.x[-1] - self.x[-2]
        dw = grad_f(self.x[-2]) - grad_f(self.x[-1])
        return A - np.outer(dx, dx) / np.dot(dw, dx) - A.dot(np.outer(dw, dw)).dot(A.transpose()) / (
            np.dot(dw, A.dot(dw)))

    def solve(self, x_0, eps):
        self.x = [np.asarray(x_0)]
        self.iters = 0
        fib_nums = fib(self.fib_iter_num)
        grad = None
        A = np.eye(2)
        while norm(grad) >= eps:
            grad = grad_f(self.x[-1])
            p = A.dot(grad)
            alpha = fib_min(fib_nums, self.x[-1], p)
            self.x.append(self.x[-1] - alpha * p)
            self.iters += 1
            if self.iters % 2 == 0:
                A = self.refresh_matrix(A)
        return self.x[-1]