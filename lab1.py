"""
Первая лабораторная работа: реализация программы, решающая задачи линенйного программирования. Технические задания:

Реализовать алгоритмы решения прямой и двойственной задач линейного программирования методами перебора опорных векторов и табличных симплекс-методом;
Предусмотреть автоперевод вводимой задачи линейного программирования в каноническую форму и двойственную задачу линейного программирования;
Предусмотреть защиту от зацикливания в алгоритме симплекс-метода (правило Бленда);
(в рамках курса) Вывести комментарий, поясняющий соответствие алгоритмов табличного симплекс-метода с тем, который изучали на лекциях.
В качестве задачи для проверки выбрать следующую задачу линейного программирования:

задача должна содержать 6 переменных неизвестных;
задача должна содержать 6 ограничений: 3 ограничения со знаком '=', 2 - c '>=', а 1 - с знаком '<=';
3 переменных имеют ограничение на знак;
целевую функцию можно как минимизировать, так и максимизировать.
"""

# стандартная форма - ИЩЕМ МИНИМУМ


import copy # для создания глубоких копий списков
from itertools import combinations
import numpy as np
EPS = 0.000000001

"""
Чтение файла. Сохраняем систему.
Предполагается, что в строке, начинающейся с goal_gunc, записана целевая функция.
В строке, начинающейся с idx, записаны индексы переменных, имеющих ограничение на знак >= 0.
"""
def read_file(filename):
    system = []
    sign = []
    goal_func = []
    idx = []
    with open(filename, "r") as f:
        for line in f.readlines():
            expression = line.split()
            if expression[0] == "goal_func":
                expression.remove("goal_func")
                for value in expression:
                    goal_func.append(float(value))
                continue
            if expression[0] == "idx":
                expression.remove("idx")
                for value in expression:
                    idx.append(int(value))
                continue
            clean_data = []
            for value in expression:
                if value.isdigit() or value[0] == '-':
                    clean_data.append(float(value))
                else:
                    sign.append(value)
            system.append(clean_data)
    return system, sign, goal_func, idx


def to_canonical(system, sign, goal_func, idx):
    # копирование данных, чтобы исходные остались прежними
    copy_sign = copy.deepcopy(sign)
    copy_system = copy.deepcopy(system)
    copy_idx = copy.deepcopy(idx)
    copy_goal_func = copy.deepcopy(goal_func)
    # приводим к канонической форме
    # сначала заменяем все знаки на равенства
    for i in range(len(copy_system)):
        if copy_sign[i] == '<=':
            for j in range(len(copy_system)):
                if j == i:
                    copy_system[j].insert(-1, 1.0)
                    copy_idx.append(len(copy_system[j]) - 2)
                else:
                    copy_system[j].insert(-1, 0.0)
            copy_goal_func.append(0.0)
            copy_sign[i] = '='
        if copy_sign[i] == '>=':
            for j in range(len(copy_system)):
                if j == i:
                    copy_system[j].insert(-1, -1.0)
                    copy_idx.append(len(copy_system[j]) - 2)
                else:
                    copy_system[j].insert(-1, 0.0)
            copy_goal_func.append(0.0)
            copy_sign[i] = '='
    # теперь переменные без ограничения на знак заменяем новыми
    # в том числе в ф-ии цели
    to_delete = []
    for i in range(len(copy_system[0]) - 1):
        if i not in copy_idx:
            # значит на знак нет ограничения
            for j in range(len(copy_system)):  # заменяем переменную без ограничения на u-v
                copy_system[j].insert(-1, copy_system[j][i])
                copy_system[j].insert(-1, -copy_system[j][i])
            copy_goal_func.insert(-1, copy_goal_func[i])
            copy_goal_func.insert(-1, -copy_goal_func[i])
            to_delete.append(i)
    to_delete = to_delete[::-1]
    for i in range(len(copy_system)):
        for j in to_delete:
            copy_system[i].pop(j)
    for j in to_delete:
        copy_goal_func.pop(j)
    copy_idx = [i for i in range(len(copy_system[0]) - 1)]
    return copy_system, copy_sign, copy_goal_func, copy_idx


def direct_to_dual(system, sign, goal_func, idx):
    dual_func = []
    dual_idx = []
    dual_sign = []
    for exp in system:
        dual_func.append(exp[-1])

    # создаем двойственную систему
    dual_system = list(map(list, zip(*system))) #транспонированная матрица
    dual_system.pop(-1)
    for i in range(len(dual_system)):
        dual_system[i].append(goal_func[i]) # добавляем свободные члены
        if i in idx: # и смотрим знаки новой системы
            dual_sign.append('<=')
        else:
            dual_sign.append('=')
        if sign[i] == '>=':
            dual_idx.append(i)
        if sign[i] == '<=':
            dual_idx.append(-i) # если idx отрицательный, значит x[i] <= 0, если idx положит, то x[i] >= 0
    return dual_system, dual_sign, dual_func, dual_idx


def get_basis_mtrxs(A : np.ndarray):
    N = A.shape[0]
    M = A.shape[1]

    basis_matrs = []
    basis_combinations_indexes = []
    all_indexes = [i for i in range(M)]

    for i in combinations(all_indexes, N):
        basis_matr = A[:, i]
        if np.linalg.det(basis_matr) != 0: # проверяем, что определитель отличен от нуля
            basis_matrs.append(basis_matr) # получаем все такие матрицы и их индексы
            basis_combinations_indexes.append(i)

    return basis_matrs, basis_combinations_indexes


def get_vectors(A : list, b : list):
    N = len(A[0])
    M = len(A)
    vectors = []

    if M >= N:  # Рассматривается матрица A[M,N}, где число строк меньше числа столбцов (M < N)
        return vectors
    else:
        basis_matrs, basis_combinations_indexes = get_basis_mtrxs(np.array(A))

    for i in range(len(basis_matrs)):  # Для всех матриц с ненулевым определителем
        solve = np.linalg.solve(basis_matrs[i], b) # Решаем систему вида A[M,N_k]*x[N]=b[M]
        if (len(solve[solve < -1 * EPS]) != 0) or (len(solve[solve > 1e+15]) != 0):
            continue

        vec = [0 for i in range(N)] # Дополняем нулями до N
        for j in range(len(basis_combinations_indexes[i])):
            vec[basis_combinations_indexes[i][j]] = solve[j]
        vectors.append(vec)
    return vectors


def brute_force(A : list, b : list, c : list):
    vectors = get_vectors(A, b)  # получаем все возможные опорные вектора
    if len(vectors) == 0:  # если их нет, нет оптимального решения
        return []

    solution = vectors[0]
    goal_min = np.dot(solution, c)  # значение фонкции цели в крайней точке

    for vec in vectors: # находим минимум
        if np.dot(vec, c) < goal_min:
            goal_min = np.dot(vec, c)
            solution = vec

    return solution


def getAb(system):
    A=[]
    b=[]
    for exp in system:
        b.append(exp[-1])
        A.append(exp[:-1])
    return A,b


def print_system(system, sign, goal_func, idx):
    A, b = getAb(system)
    print('A:')
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], '*x[',j, ']', end='', sep='')
            if (j != len(A[i]) - 1):
                print(' + ', end='')
        print(' ', sign[i], ' ', b[i])
    print('Целевая функция: ', goal_func)
    print('Индексы переменных с ограничением на знак: ', idx)
    print('\n')







system, sign, goal_func, idx = read_file("task.txt")
print('---ИСХОДНАЯ ЗАДАЧА---')
print_system(system, sign, goal_func, idx)

print('---ДВОЙСТВЕННАЯ ЗАДАЧА---')
system1, sign1, goal_func1, idx1 = direct_to_dual(system, sign, goal_func, idx)
print_system(system1, sign1, goal_func1, idx1)

print('---КАНОНИЧЕСКАЯ ФОРМА ИСХОДНОЙ ЗАДАЧИ---')
system2, sign2, goal_func2, idx2 = to_canonical(system, sign, goal_func, idx)
print_system(system2, sign2, goal_func2, idx2)

print('---КАНОНИЧЕСКАЯ ФОРМА ДВОЙСТВЕННОЙ ЗАДАЧИ---')
system3, sign3, goal_func3, idx3 = to_canonical(system1, sign1, goal_func1, idx1)
print_system(system3, sign3, goal_func3, idx3)

print('---РЕШЕНИЕ МЕТОДОМ ПЕРЕБОРА ОПОРНЫХ ВЕКТОРОВ---')
A, b = getAb(system2)
solution = brute_force(A, b, goal_func2)
print(solution)
print('\n')

print('---РЕШЕНИЕ СИМПЛЕКС-МЕТОДОМ---')



