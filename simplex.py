import math
import numpy as np

def to_tableau(c, A, b):
    # Преобразование в таблицу симплекс метода:
    # __________________
    # |             |   |
    # |      A      | b |
    # |             |   |
    # -------------------
    # |      c      | 0 |
    # -------------------
    for i in range(len(c)):
        c[i] = -1 * c[i]

    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    return xb + [z]

def can_be_improved(tableau):
    # Проверяем, где можно увеличить неосновные значения, не уменьшая значение целевой функции.
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])

def get_pivot_position(tableau):

    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)

    restrictions = []

    # Если значение целевой функции можно улучшить, мы ищем точку разворота.
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    # Если нет - задача неограничена
    if (all([r == math.inf for r in restrictions])):
        raise Exception("Linear program is unbounded.")

    row = restrictions.index(min(restrictions))
    return row, column


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for eq in tableau]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value

    # делаем поворотный шаг и возвращаем новую таблицу
    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier

    return new_tableau


def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1


def get_solution(tableau):
    # извлекаем решение из таблицы
    columns = np.array(tableau).T
    solutions = []
    for column in columns[:-1]:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)

    return solutions


def simplex(c, A, b):
    tableau = to_tableau(c, A, b)

    # пока можем улучшать целевую функцию - делаем поворот
    while can_be_improved(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)

    return get_solution(tableau)