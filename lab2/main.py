import numpy as np

from brute_force import solve_brute_force
from canon import to_canon
from closing import make_closed_tp
from input import input_
from prints import print_solution_tp, print_problem
from transport_simplex import transportation_simplex_method


def main():
    supply, demand, costs, \
    penalties_for_more_demand, \
    penalties_for_more_supply = input_("input.txt")

    print("Исходная транспортная задача:")
    print_problem(supply, demand, costs)


    # штрафы за неудовлетворение спроса
    penalties_for_more_demand = [0,0,0,0,0]
    # штрафы за непокрытие предложения
    penalties_for_more_supply = [0,0,0,0]

    if all(penalties == 0 for penalties in penalties_for_more_demand) and\
            all(penalties == 0 for penalties in penalties_for_more_supply):
        print("В задаче нет штрафов за неудовлетворение спроса и предложения. \n")
    else:
        if any(penalties == 0 for penalties in penalties_for_more_demand):
            print("Штраф за неудовлетворение спроса:")
            print(penalties_for_more_demand)
        if any(penalties == 0 for penalties in penalties_for_more_supply):
            print("Штраф за неудовлетворение предложения:")
            print(penalties_for_more_supply)


    # приводим задачу в закрытую форму
    closed_supply, closed_demand, closed_costs = make_closed_tp(supply, demand, costs,
                                                                penalties_for_more_demand,
                                                                penalties_for_more_supply)

    solution = transportation_simplex_method(closed_supply, closed_demand, closed_costs)

    print_solution_tp(costs, solution)

    print("Решение методом перебора опорных точек")

    min_task, A_matr, b_vec = to_canon(len(closed_supply), len(closed_demand), closed_supply, closed_demand, closed_costs)
    # удалить последнюю строчку
    A_matr.pop(len(A_matr) - 1)
    b_vec.pop(len(b_vec) - 1)
    brute_solution = solve_brute_force(A_matr, b_vec, min_task, 0)
    brute_solution = np.reshape(brute_solution, (len(closed_supply), len(closed_demand)))
    print(brute_solution)

    print_solution_tp(costs, brute_solution)
main()