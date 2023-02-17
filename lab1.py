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

"""
Чтение файла. Сохраняем систему.
Предполагается, что в строке, начинающейся с goal_gunc, записана целевая функция.
В строке, начинающейся с idx, записаны индексы переменных, имеющих ограничение на знак >= 0.
"""

# ИЩЕМ МИНИМУМ


import copy # для создания глубоких копий списков


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
    print('system:')
    for exp in copy_system:
        print(exp)
    print('sign: ', copy_sign)
    print('goal_func: ', copy_goal_func)
    print('idx: ', copy_idx)
    print('\n')
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








system, sign, goal_func, idx = read_file("task1.txt")
for exp in system:
    print(exp)
print('sign: ', sign)
print('goal_func: ', goal_func)
print('idx: ', idx)
print('\n')
system, sign, goal_func, idx = to_canonical(system, sign, goal_func, idx)
print('\n')
print('system:')
for exp in system:
    print(exp)
print('sign: ', sign)
print('goal_func: ', goal_func)
print('idx: ', idx)
print('\n')



