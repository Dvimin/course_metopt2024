import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def make_data():
    x, y = np.meshgrid(np.arange(0, 10, 0.05), np.arange(0, 10, 0.05))
    z = 5 * x + y + 4 * np.sqrt(1 + x ** 2 + 3 * y ** 2)
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
    #surface()
    plot_lines([0.0, 3.0, 2.0, 4], [0.0, 2.1, 3.5, 6])

