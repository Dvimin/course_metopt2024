import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def f(x):
    return 4*x[0] + x[1] + 4*np.sqrt(1+3*x[0]**2+x[1]**2) + x[2]**3


def restrictions():
    # Создание сетки для отображения поверхности
    x = np.linspace(-0.5, 0.5, 100)
    y = np.linspace(-0.5, 0.5, 100)
    x, y = np.meshgrid(x, y)

    # Ограничение x_1^2 + x_2^2 <= 1
    z1 = np.sqrt(1 - x ** 2 - y ** 2)

    # Ограничение 4x_1^2 + 4x_2 - 3 <= 0
    z2 = (-4 * x ** 2 - 4 * y + 3) / 4

    # Ограничение 4x_1^2 + 4x_2 + 3 <= 0
    z3 = (-4 * x ** 2 - 4 * y - 3) / 4

    # Ограничение 1 - x_3 <= 0
    z4 = 1 - x

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Отображение ограничений
    ax.plot_surface(x, y, z1, color='gray', alpha=0.5)
    ax.plot_surface(x, y, z2, color='red', alpha=0.5)
    ax.plot_surface(x, y, z3, color='blue', alpha=0.5)
    ax.plot_surface(x, y, z4, color='green', alpha=0.5)

    # Настройка графика
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.set_zlabel('$x_3$')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 1)

    # Отображение легенды
    gray_patch = plt.plot([], [], ' ', color='gray', label='$x_1^2 + x_2^2 \leq 1$')
    red_patch = plt.plot([], [], ' ', color='red', label='$4x_1^2 + 4x_2 - 3 \leq 0$')
    blue_patch = plt.plot([], [], ' ', color='blue', label='$4x_1^2 + 4x_2 + 3 \leq 0$')
    green_patch = plt.plot([], [], ' ', color='green', label='$1 - x_3 \leq 0$')
    plt.legend(handles=[gray_patch[0], red_patch[0], blue_patch[0], green_patch[0]])

    plt.show()

if __name__ == '__main__':
    restrictions()