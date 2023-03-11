from closing import make_closed_tp
from input import input_
from prints import print_solution_tp
from transport_simplex import transportation_simplex_method


def main():
    supply, demand, costs, \
    penalties_for_more_demand, \
    penalties_for_more_supply = input_("input.txt")

    # штрафы за неудовлетворение спроса
    penalties_for_more_demand = [0,0,0,0,0]
    # штрафы за непокрытие предложения
    penalties_for_more_supply = [0,0,0,0]

    # приводим задачу в закрытую форму
    closed_supply, closed_demand, closed_costs = make_closed_tp(supply, demand, costs,
                                                                penalties_for_more_demand,
                                                                penalties_for_more_supply)

    solution = transportation_simplex_method(closed_supply, closed_demand, closed_costs)

    print_solution_tp(costs, solution)



main()