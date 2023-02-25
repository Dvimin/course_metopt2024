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
    print('to_canonical: ')
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


class SimplexMethod:

    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c

    def solve(self):
        m = len(self.A)
        n = len(self.A[0])

        c_b = []
        pos = 0

        for i in range(n):
            sum = 0
            basic = True
            col = get_col(self.A, i)
            for elem in col:
                sum += elem
                if elem > 1 | elem < 0:
                    basic = False
            if sum == 1 & basic:
                c_b[pos] = self.c[i]

        reduced_costs = compute_costs(c_b, self.A, self.c)
        z = mult_vectors(c_b, self.b)

        tableau = [[]]
        for i in range(len(reduced_costs)):
            tableau[0].append(reduced_costs[i])
        tableau[0].append(z)

        for i in range(m):
            tableau.append([])
            for j in range(n):
                tableau[i+1].append(self.A[i][j])
            tableau[i+1].append(self.b[i])

        timer = 0

        while timer < 300:
            optimal = True
            most_negative_index = 0
            for i in range(len(tableau[0]) - 1):
                if tableau[0][i] < 0:
                    optimal = False
                    if tableau[0][i] < tableau[0][most_negative_index]:
                        most_negative_index = i
            if optimal:
                optimal_sol = []

                for i in range(n):
                    col = get_col(tableau, i)
                    sum = 0
                    basic = True
                    for elem in col:
                        sum += elem
                        if elem > 1 | elem < 0 | sum > 1:
                            basic = False
                    if basic:
                        b_index = -1
                        for j in range(len(col)):
                            if col[j] == 1:
                                b_index = j
                        optimal_sol[i] = tableau[b_index][len(tableau[0]) - 1]
                    else:
                        optimal_sol[i] = 0

                return 1, optimal_sol, tableau[0][len(tableau[0]) - 1]

            pivot_index = 1
            min_ratio = 9999999
            for i in range(1, len(tableau)):
                if tableau[i][most_negative_index] > 0:
                    if tableau[i][len(tableau[0]) - 1] / tableau[pivot_index][most_negative_index] < min_ratio:
                        pivot_index = 1
                        min_ratio = tableau[i][len(tableau[0]) - 1] / tableau[pivot_index][most_negative_index]
            if pivot_index == 1 & tableau[pivot_index][most_negative_index] <= 0:
                return -3

            bland = True
            if bland:
                for i in range(len(tableau[0]) - 1):
                    if tableau[0][i] < 0:
                        most_negative_index = i
                        break

            tableau = pivot(tableau, pivot_index, most_negative_index)

            timer += 1

        return 0


def pivot(tableau, r, c):
    if tableau[r][c] != 1:
        divisor = tableau[r][c]
        for i in range(len(tableau[r])):
            tableau[r][c] = tableau[r][i] / divisor

    for i in range(r):
        if tableau[i][c] != 0:
            factor = -tableau[i][c]
            for j in range(len(tableau[0])):
                tableau[i][j] = tableau[i][j] + factor * tableau[r][j]

    for i in range(r + 1, len(tableau)):
        if tableau[i][c] != 0:
            factor = -tableau[i][c]
            for j in range(len(tableau[0])):
                tableau[i][j] = tableau[i][j] + factor * tableau[r][j]

    return tableau


def get_col(A, inx):
    n = len(A)
    col = []
    for i in range(n):
        col.append(A[i][inx])
    return col


def mult_vectors(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result


def compute_costs(c_b, A, objective_vals):
    n = len(A[0])
    reduced_costs = []
    for i in range(n):
        reduced_costs[i] = mult_vectors(c_b, get_col(A, i)) - objective_vals[i]
    return reduced_costs

EPS = 0.000000001

def get_basis_matrs(A : np.ndarray):
    N = A.shape[0]
    M = A.shape[1]

    basis_matrs = []
    basis_combinations_indexes = []
    all_indexes = [i for i in range(M)]

    for i in combinations(all_indexes, N):
        basis_matr = A[:, i]
        if np.linalg.det(basis_matr) != 0:
            basis_matrs.append(basis_matr)
            basis_combinations_indexes.append(i)
        #basis_matrs.append(basis_matr)
        #basis_combinations_indexes.append(i)

    return basis_matrs, basis_combinations_indexes

def get_all_possible_vectors(A : list, b : list):
    N = len(A[0])
    M = len(A)
    vectors = []

    if M >= N:
        return vectors
    else:
        basis_matrs, basis_combinations_indexes = get_basis_matrs(np.array(A))

    for i in range(len(basis_matrs)):
        solve = np.linalg.solve(basis_matrs[i], b)
        if (len(solve[solve < -1 * EPS]) != 0) or (len(solve[solve > 1e+15]) != 0):
            continue

        vec = [0 for i in range(N)]
        for j in range(len(basis_combinations_indexes[i])):
            vec[basis_combinations_indexes[i][j]] = solve[j]
        vectors.append(vec)
    return vectors


def solve_brute_force(A : list, b : list, c : list):
    vectors = get_all_possible_vectors(A, b)
    if len(vectors) == 0:
        return []

    solution = vectors[0]
    target_min = np.dot(solution, c)

    for vec in vectors:
        if np.dot(vec, c) < target_min:
            target_min = np.dot(vec, c)
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
    for exp in A:
        print(exp)

    print('b:')
    for exp in b:
        print(exp, end=' ')
    print('\n')
    print('sign: ', sign)
    print('goal_func: ', goal_func)
    print('idx: ', idx)
    print('\n')







system, sign, goal_func, idx = read_file("task1.txt")
print('---ИСХОДНАЯ ЗАДАЧА---')
print_system(system, sign, goal_func, idx)
print('---КАНОНИЧЕСКАЯ ФОРМА---')
system, sign, goal_func, idx = to_canonical(system, sign, goal_func, idx)
print_system(system, sign, goal_func, idx)
print('---РЕШЕНИЕ МЕТОДОМ ПЕРЕБОРА ОПОРНЫХ ВЕКТОРОВ---')
A, b = getAb(system)
solution = solve_brute_force(A, b, goal_func)
print(solution)
print('---РЕШЕНИЕ СИМПЛЕКС-МЕТОДОМ---')
smplx = SimplexMethod(A, b, goal_func)
print(smplx.solve())



