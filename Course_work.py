import random
from Course_work_ant import AntColonyAlgorithm
from Course_work_din import din_method
import matplotlib.pyplot as plt
import networkx as nx
import time


def plot_graph_with_path(ax, time_matrix, path, city_classes, method):
    G = nx.Graph()
    for i in range(len(time_matrix)):
        for j in range(i + 1, len(time_matrix)):
            if time_matrix[i][j] > 0:
                G.add_edge(i, j, weight=time_matrix[i][j])

    pos = nx.spring_layout(G)

    colors = ['blue' if city_classes[node] == 1 else 'green' if city_classes[node] == 2 else 'red' for node in
              G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold', ax=ax)

    # Рисуем ребра
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), alpha=0.3, ax=ax)

    # Подсвечиваем путь
    edges_in_path = list(
        zip(path, list(path[1:]) + [path[0]]))
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=2, ax=ax)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    ax.set_title(f'{method} {len(time_matrix)}x{len(time_matrix)} Graph with highlighted path')
    ax.axis('off')


def generate_time_matrix(size):
    matrix = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
    # Создаем симметричную матрицу
    for i in range(size):
        for j in range(i, size):
            matrix[i][j] = matrix[j][i] = random.randint(1, 10) if i != j else 0
    return matrix


# def generate_city_classes_and_requirements(size, n_classes=3):
#     # Убедимся, что для каждого класса есть достаточно городов
#     min_cities_per_class = size // n_classes
#     city_classes = []
#     for i in range(1, n_classes + 1):
#         city_classes += [i] * min_cities_per_class
#
#     # Если размер матрицы не делится нацело на количество классов, добавим оставшиеся города
#     remaining_cities = size % n_classes
#     for i in range(1, remaining_cities + 1):
#         city_classes.append(i)
#
#     # Перемешаем классы городов для разнообразия
#     random.shuffle(city_classes)
#
#     # Учитывая переменную размерность городов на класс,
#     # зададим требования так, чтобы не превысить количество городов в наименьшем классе
#     class_counts = [city_classes.count(c)-1 for c in range(1, n_classes + 1)]
#     min_class_count = min(class_counts)
#     class_requirements = {i: min_class_count for i in range(1, n_classes + 1)}
#
#     return city_classes, class_requirements

def generate_city_classes_and_requirements(size, n_classes=3):
    min_cities_per_class = size // n_classes
    city_classes = []
    for i in range(1, n_classes + 1):
        city_classes += [i] * min_cities_per_class

    remaining_cities = size % n_classes
    for i in range(1, remaining_cities + 1):
        city_classes.append(i)

    random.shuffle(city_classes)

    class_counts = {cls: city_classes.count(cls) for cls in range(1, n_classes + 1)}

    class_requirements = {cls: random.randint(1, count) for cls, count in class_counts.items()}

    return city_classes, class_requirements


sizes = [5, 7, 12]
# sizes = [i for i in range(3, 14)]
# Initialize lists to collect statistics
aco_costs = []
aco_times = []
din_costs = []
din_times = []

# for size in sizes:
    # time_matrix = generate_time_matrix(size)
    # city_classes, class_requirements = generate_city_classes_and_requirements(size)
time_matrix = [
    [0, 2, 3, 4, 6, 1],
    [2, 0, 7, 5, 3, 3],
    [3, 7, 0, 2, 5, 2],
    [4, 5, 2, 0, 6, 6],
    [6, 3, 5, 6, 0, 9],
    [1, 3, 2, 6, 9, 0],
]
city_classes = [1, 2, 3, 1, 2, 3]
class_requirements= {1: 2, 2: 1, 3: 2}
print(f"Time Matrix:{5}x{5}")
for row in time_matrix:
    print(row)
print("City Classes:", city_classes)
print("Class Requirements:", class_requirements)

fig, axs = plt.subplots(1, 2, figsize=(16, 6))

print("\nRunning Ant Colony Algorithm...")
start_time = time.time()
aco_algorithm = AntColonyAlgorithm(time_matrix, city_classes, class_requirements, n_ants=100, n_best=10,
                                   n_iterations=100, decay=0.5, alpha=1, beta=2)
shortest_path, cost = aco_algorithm.run()
end_time = time.time()
aco_costs.append(cost)
aco_times.append(end_time - start_time)
print("Shortest path: ", shortest_path)
print("Cost of the path: ", cost)
print(f"Time taken: {end_time - start_time} seconds")
plot_graph_with_path(axs[0], time_matrix, shortest_path, city_classes, 'ANT')
print("-------------------------------------")

print("\nRunning Dynamic Programming Method...")
start_time = time.time()
din_result, din_route = din_method(time_matrix, city_classes, class_requirements)
end_time = time.time()
din_costs.append(din_result)
din_times.append(end_time - start_time)
print("Shortest path: ", din_route)
print("Cost of the path: ", din_result)
print(f"Time taken: {end_time - start_time} seconds")
plot_graph_with_path(axs[1], time_matrix, din_route, city_classes, 'DIN')

plt.show()

print("=====================================\n")

# After the loop over sizes

# Statistical plot showing comparison of times
plt.figure(figsize=(10, 5))
plt.plot(sizes, aco_times, label='Ant Colony Time')
plt.plot(sizes, din_times, label='DIN Time')
plt.xlabel('Problem Size')
plt.ylabel('Time (seconds)')
plt.title('Time Comparison b/w Ant Colony and DIN')
plt.legend()
plt.show()
