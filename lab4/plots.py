import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import grad
import grad_dfp


def make_data():
    x, y = np.meshgrid(np.arange(-0.4, 0, 0.01), np.arange(-0.3, 0.1, 0.01))
    z = 4 * x + y + 4 * np.sqrt(1 + 3*x ** 2 + y ** 2)
    return x, y, z


def surface():
    x, y, z = make_data()
    fig = plt.figure()
    axes = fig.add_subplot(projection='3d')
    axes.plot_surface(x, y, z, edgecolor='k', linewidth=0.1, cmap=cm.coolwarm, antialiased=False)
    plt.show()


def plot_lines(points_x=None, points_y=None):
    x, y, z = make_data()
    cs = plt.contour(x, y, z, 15)
    plt.clabel(cs, colors="black")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Линии уровня функции")
    plt.plot(points_x, points_y, 'bX--')
    plt.show()


if __name__ == '__main__':
    x, y, solution, iters = grad.solve(np.array([0, 0]), 0.0001)

    #print(grad_dfp.solve(np.array([0, 0]), 0.001))
    plot_lines(x, y)
    x, y, solution, iters = grad_dfp.solve(np.array([0, 0]), 0.0001)

    #print(grad_dfp.solve(np.array([0, 0]), 0.001))
    plot_lines(x, y)