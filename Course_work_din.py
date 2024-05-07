import itertools


def din_method(time_matrix, city_classes, class_requirements):
    n = len(time_matrix)
    start = 0
    route_count = 0

    city_combinations_per_class = {
        cls: [city for city in range(n) if city_classes[city] == cls]
        for cls in class_requirements
    }

    valid_routes = itertools.product(
        *(itertools.combinations(city_combinations_per_class[cls], class_requirements[cls])
          for cls in class_requirements)
    )

    min_route_cost = float('inf')
    min_route = []

    for route_combination in valid_routes:
        for route in itertools.permutations([city for cls_route in route_combination for city in cls_route]):
            route_count += 1
            # current_route_cost = sum(time_matrix[city][next_city] for city, next_city in
            #                          zip((start,) + route, route + (start,)))
            current_route_cost = 0
            for i in range(-1, len(route)-1):
                current_route_cost += time_matrix[route[i]][route[i+1]]

            # print(f"Checking route {route_count}: {route}, cost: {current_route_cost}")

            if current_route_cost < min_route_cost:
                min_route_cost = current_route_cost
                min_route = route
                print(f"New best route found: {route} with cost: {current_route_cost}")

    print(f"Total routes checked: {route_count}")
    return min_route_cost, min_route
