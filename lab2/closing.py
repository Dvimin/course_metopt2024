# функция перевода транспортной задачи в закрытую форму
def make_closed_tp(supply, demand, costs,
                   penalties_for_more_demand,
                   penalties_for_more_supply):

    # всего предложения
    total_supply = sum(supply)
    # всего спроса
    total_demand = sum(demand)

    # если спроса больше, то вводим штрафы за неустойку
    if total_supply < total_demand:
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [penalties_for_more_demand]
        return new_supply, demand, new_costs

    # если
    if total_supply > total_demand:
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs
        for i in range(len(new_costs)):
            new_costs[i].append(penalties_for_more_supply[i])
        return supply, new_demand, new_costs

    return supply, demand, costs