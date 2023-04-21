import numpy as np
import matplotlib.pyplot as plt
from numpy import fabs

import Task as t
from lab3.GoldenRatio import GoldenRatioSolver
from lab3.SecondaryPoint import SecondaryPointSolver
from lab3.UniformSearch import UniformSearchSolver


def unimodal():
    task = t.Task()
    fig, ax = plt.subplots()
    plt.rcParams['text.usetex'] = True
    x = np.linspace(task.a, task.b, 10_000)
    y = [task.func(val) for val in x]
    ax.plot(x, y)
    ax.set_title(r'$f(x) = \frac{x*\sqrt{1-x}}{1+x}$')
    plt.grid()
    plt.savefig('uni.png')


def func_call_count():
    u = []
    g = []
    s = []
    for eps in 0.1, 0.01, 0.001:
        task = t.Task()
        uss = UniformSearchSolver(task)
        uss.solve(eps)
        u.append(uss.func_call_count)
        task = t.Task()
        grs = GoldenRatioSolver(task)
        grs.solve(eps)
        g.append(grs.func_call_count)
        task = t.Task()
        sps = SecondaryPointSolver(task)
        sps.solve(eps)
        s.append(sps.func_call_count)
    eps = [0.1, 0.01, 0.001]
    fig, ax = plt.subplots()
    ax.plot(eps, u, label='Метод равномерного поиска', linestyle='--')
    ax.plot(eps, g, label='Метод золотого сечения', linestyle='-.')
    ax.plot(eps, s, label='Метод пробных точек', linestyle=':')
    ax.set_title(r'Зависимость кол-ва вызова функции от заданной точности')
    ax.legend()
    plt.grid()
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('func_call.png')


def accuracy():
    u = []
    g = []
    s = []
    for eps in 0.1, 0.01, 0.001:
        task = t.Task()
        print(task.x_max)
        uss = UniformSearchSolver(task)
        print(uss.solve(eps))
        u.append(fabs(uss.solve(eps) - task.x_max))
        task = t.Task()
        grs = GoldenRatioSolver(task)
        g.append(fabs(grs.solve(eps) - task.x_max))
        task = t.Task()
        sps = SecondaryPointSolver(task)
        s.append(fabs(sps.solve(eps) - task.x_max))
    eps = [0.1, 0.01, 0.001]
    fig, ax = plt.subplots()
    ax.plot(eps, g, label='Метод золотого сечения', linestyle='--')
    ax.plot(eps, s, label='Метод пробных точек', linestyle='-.')
    ax.plot(eps, u, label='Метод равномерного поиска', linestyle=':')
    ax.plot(eps, eps, label='Диагональ', linestyle='-')
    ax.set_title(r'Зависимость ошибки от заданной точности')
    ax.legend()
    plt.grid()
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('accuracy.png')


func_call_count()
accuracy()
unimodal()
