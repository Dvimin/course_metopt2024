import numpy as np
from typing import List
import task as t
from scipy.optimize import linprog

# функция нахождения начального приближения, допустимого для задачи
def validatex0(x0):
    # имеем похожий алгоритм Зойтендейка, но со следующими условиями:
    # min eta
    # phi_i(x) <= eta, i = 1,2,...,m , m - количество ограничений
    eta = max([r(x0) for r in t.restrictions])
    if eta < 0:
        return x0

    valid = False
    # если входящее значение не удовлетворяет условиям
    # находим начальное приближение
    while not valid:
        # решаем вспомогательную задачу ЛП
        # находим новый параметр eta
        delta = -eta
        res = simplex(x0, delta)
        s, eta = res.x[0:3], res.fun
        valid = False
        alpha = 1
        lyambda = 0.5

        while not valid:
            # соласно методу зойтендейка будем делатьь шаг по альфа и проверять условие
            valid = t.f(x0 + alpha * s) <= t.f(x0) + lyambda * eta * alpha
            for r in t.restrictions:
                valid = valid and r(x0 + alpha * s) <= 0
                if not valid:
                    break

            if not valid:
                # уменьшаем шаг по принципу дробления
                alpha *= lyambda
                if alpha < pow(2, -10):
                    alpha = lyambda
                    break

        # если x_0 не подходит, делаем шаг
        # и делаем данный шаг по найденному направлению
        x0 += alpha * s
        print(f"x0: {x0}")

    return x0


# функция нахождения множества номеров ограничений
# вероятность нарушения которых в окрестности delta высока
# то есть для i принадлежащих этому множеству, выполнено нер-во
# -delta <= phi_i(x) <= 0
def get_bounds(x, delta):
    res = []
    for idx in range(len(t.restrictions)):
        if -delta <= t.restrictions[idx](x) <= 0.0:
            res.append(idx)
    return res


# Выбор величины шага по принципу дробления
def get_step(x, eta, s):
    # alpha_0 = 1
    alpha = 1

    # Необходимо выполнения условий:
    # phi_0(x_k + alpha_k * s_k) - phi_0(x_k) <= eta_k*alpha_k, phi_0 - функция цели
    # phi_i(x_k + alpha_k * s_k) <= 0, i - номер ограничения(проходимся по всем активным)
    while True:
        # проверяем выполнение неравенства для функции цели
        first_eq = t.f([x_k + alpha * s_k for x_k, s_k in zip(x, s)]) - t.f(x) <= 0.5 * eta * alpha

        second_eq = True
        # проверяем выполнения неравенств для ограничений
        for r in t.restrictions:
            second_eq = second_eq and (r([x_k + alpha * s_k for x_k, s_k in zip(x, s)]) <= 0)

        # если ограничения выполнены, то возвращаем шаг
        if first_eq and second_eq:
            return alpha
        # иначе уменьшаем шаг
        alpha *= 0.5


def simplex(x_k, d_k):
    # составим задачу ЛП

    # найдем множество индексов ближайших ограничений
    bounds_idxs = get_bounds(x_k, d_k)

    # создадим матрицу А со знаками <=
    A_ub = np.zeros(shape=(1 + len(bounds_idxs), 4))

    A_ub[:, 3] = -1
    # заполним первую строку градиентом минимизируемой функции
    A_ub[0, 0:3] = t.grad_f(x_k)

    # заполним остальные строки градиентами ограничений
    j = 1
    for i in bounds_idxs:
        A_ub[j, 0:3] = t.restrictions_grad[i](x_k)
        j += 1

    # будем минимизировать параметр eta
    c = np.zeros(4)
    c[3] = 1

    b_ub = np.zeros(A_ub.shape[0])
    # введем ограничения на s : ||s|| <= 1
    bounds = [[-1, 1], [-1, 1], [-1, 1], [None, None]]

    # решим поставленную задачу ЛП и найдем направление спуска и значение eta
    return linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')


def zoytendeyk(x0: List[float], eta: int) -> List[float]:
    # Начальный этап
    # Выберем lyambda = 1/2
    # Выберем критерий близости delta_0 = -eta_0, delta_0 > 0
    # Выберем начальное приближение, входящее в область допустимых значений
    lam = 0.5
    delta = -eta
    x = x0

    iter = -1

    # Основной этап
    while True:
        iter += 1
        # Имеем x_k и delta_k

        # Найдем направление спуска s, решив ЗЛП
        *s, eta = simplex(x, delta).x

        # eta < delta => делаем шаг aplha_k, по выбранному направлению s_k
        # eta > delta => шаг не делаем, меняем дельту
        if eta < delta:
            # найдем шаг
            alpha = get_step(x, eta, s)
            # делаем шаг x_{k+1} = x_k + alpha_k*s_k
            x = [x_k + alpha * s_k for x_k, s_k in zip(x, s)]
            # delta не меняем
        else:
            # меняем дельту
            delta *= lam

        print(f"iter: {iter} - x: {x}")  # - delta: {delta} - eta: {eta} - f(x): {func(x)}")

        # если delta < всех активных ограничений от x_k и delta < eps, завершаем алгоритм
        if delta < -max([r(x) for r in t.restrictions]) and abs(eta) < 1e-5:
            break

    return x