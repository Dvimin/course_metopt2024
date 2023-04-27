"""import numpy as np

import grad
import grad_dfp
from lab4.plots import plot_lines


def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)

print(f'Заданная точность = {0.01}')
x, y, solution, iters = grad.solve(np.array([0, 0]), 0.01)
#print(x, y)
x_min, y_min = -4 / np.sqrt(87), -np.sqrt(3 / 29)


for eps in [0.001]:
    print(f'Заданная точность = {eps}')
    x, y, solution, iters = grad_dfp.solve(np.array([0,0]), eps)
    print(x)
    print(y)
    plot_lines(x, y)
    for i in range(len(x)-1):
        verh = norm([x[i+1]-x_min, y[i+1]-y_min])
        niz = norm([x[i]-x_min, y[i]-y_min])
        print('Соотношение: ', verh/niz**2)
    plot_lines(x, y)"""

import numpy as np

import grad
import grad_dfp
from lab4.plots import plot_lines


def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)

x_min, y_min = -4 / np.sqrt(87), -np.sqrt(3 / 29)
print("x_min, y_min= ", x_min, y_min)

for eps in [0.01]:
    print(f'Заданная точность = {eps}')
    # x, y, solution, iters = grad_dfp.solve(np.array([0,0]), eps)
    print("DFP:")
    solver = grad_dfp.DFP()
    solution = solver.get_solution((0.0, 0.0), eps)
    print('\tsolution: ' + str(solution))
    print('\titers: ' + str(solver.get_iter_num()))
    x = np.ndarray((1, len(solver.x)))
    y = np.ndarray((1, len(solver.x)))
    print(solver.x)
    for i in range(len(solver.x)):
        x[0, i] = solver.x[i][0]
        y[0, i] = solver.x[i][1]
    print(x[0])
    print(y[0])
    for i in range(len(x[0]) - 1):
        verh = norm([x[0,i + 1] - x_min, y[0,i + 1] - y_min])**2
        niz = norm([x[0,i] - x_min, y[0,i] - y_min])
        print('Соотношение: ', verh / niz)
    solver.draw_contoures()


