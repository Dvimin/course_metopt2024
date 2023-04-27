import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import grad
import grad_dfp
from grad import norm


def make_data():
    x, y = np.meshgrid(np.arange(-1, 0.2, 0.01), np.arange(-0.5, 0.2, 0.01))
    z = 4 * x + y + 4 * np.sqrt(1 + 3*x ** 2 + y ** 2)
    return x, y, z


def surface():
    x, y, z = make_data()
    fig = plt.figure()
    axes = fig.add_subplot(projection='3d')
    axes.plot_surface(x, y, z, edgecolor='k', linewidth=0.1, cmap=cm.Pastel2, antialiased=False)
    plt.savefig('surface.png')


def plot_lines(points_x=None, points_y=None):
    x, y, z = make_data()
    cs = plt.contourf(x, y, z, cmap=cm.Pastel2)
    plt.clabel(cs, colors="black")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Линии уровня функции")
    plt.plot(points_x, points_y, 'bX--')
    x_min, y_min = -4 / np.sqrt(87), -np.sqrt(3 / 29)
    plt.plot(x_min, y_min, 'r*')
    plt.show()


def accuracy():
    s = []
    s_dfp = []
    x_min, y_min = -4/np.sqrt(87), -np.sqrt(3/29)
    for eps in [0.1, 0.01, 0.001, 0.0001]:
        x, y, solution, iters = grad.solve(np.array([0, 0]), eps)
        s.append(norm([solution[0]-x_min, solution[1]-y_min]))
        x, y, solution, iters = grad_dfp.solve(np.array([0, 0]), eps)
        s_dfp.append(norm([solution[0]-x_min, solution[1]-y_min]))
    eps = [0.1, 0.01, 0.001, 0.0001]
    fig, ax = plt.subplots()
    ax.plot(eps, eps, label='Диагональ', linestyle='--')
    ax.plot(eps, s, label='Метод наискорейшего спуска', linestyle='-.')
    ax.plot(eps, s_dfp, label='Метод Девидона - Флетчера - Пауэлла', linestyle=':')
    ax.set_title(r'Зависимость ошибки от заданной точности')
    plt.xscale('log')
    plt.yscale('log')
    ax.legend()
    plt.grid()
    plt.show()


def iterations():
    s = []
    s_dfp = []
    for eps in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
        x, y, solution, iters = grad.solve(np.array([0, 0]), eps)
        s.append(iters)
        x, y, solution, iters = grad_dfp.solve(np.array([0, 0]), eps)
        s_dfp.append(iters)
    eps = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    fig, ax = plt.subplots()
    ax.plot(eps, s, label='Метод наискорейшего спуска', linestyle=':')
    ax.plot(eps, s_dfp, label='Метод Девидона - Флетчера - Пауэлла', linestyle='--')
    ax.set_title(r'Зависимость количества итераций от заданной точности')
    plt.xscale('log')
    ax.legend()
    plt.grid()
    plt.show()



if __name__ == '__main__':
    #surface()
    #iterations()
    #accuracy()
    x, y, solution, iters = grad.solve(np.array([0, 0]), 0.0001)
    plot_lines(x, y)

    #print(grad_dfp.solve(np.array([0, 0]), 0.001))
    x, y, solution, iters = grad_dfp.solve(np.array([0, 0]), 0.0001)

    #print(grad_dfp.solve(np.array([0, 0]), 0.001))
    #plot_lines(x, y)
