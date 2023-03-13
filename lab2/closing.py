# функция перевода транспортной задачи в закрытую форму
from prints import print_problem


def make_closed_tp(supply, demand, costs,
                   penalties_for_more_demand,
                   penalties_for_more_supply):
    print("Приведение задачи к закрытому виду...")
    # всего предложения
    total_supply = sum(supply)

    # всего спроса
    total_demand = sum(demand)

    print("Всего предложения:")
    print(total_supply)
    print("Всего спроса:")
    print(total_demand)

    # если спроса больше, то вводим штрафы за неустойку
    if total_supply < total_demand:
        print("Спрос больше предложения, закрытая задача будет иметь вид:")
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [penalties_for_more_demand]
        print_problem(new_supply, demand, new_costs)
        return new_supply, demand, new_costs

    # если
    if total_supply > total_demand:
        print("Предложение больше спроса, закрытая задача будет иметь вид:")
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs
        for i in range(len(new_costs)):
            new_costs[i].append(penalties_for_more_supply[i])

        print_problem(supply, new_demand, new_costs)
        return supply, new_demand, new_costs
    print("Спрос равен предложению, исходная задача имеет закрытый вид \n")
    return supply, demand, costs