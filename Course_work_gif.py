import matplotlib.pyplot as plt
import networkx as nx
import time
from IPython.display import clear_output
# Веса

# Size: 5x5
# Time Matrix:
# [0, 6, 5, 4, 7]
# [6, 0, 4, 8, 2]
# [5, 4, 0, 10, 5]
# [4, 8, 10, 0, 8]
# [7, 2, 5, 8, 0]
# City Classes: [2, 2, 3, 1, 1]
# Class Requirements: {1: 1, 2: 1, 3: 1}
#
# Running Ant Colony Algorithm...
# Shortest path:  [1, 2, 4]
# Cost of the path:  11
# -------------------------------------
#
# Running Dynamic Programming Method...
# Минимальная стоимость маршрута: 18
# Минимальный маршрут: (3, 0, 2)

matrix = [
    [0, 7, 9, 9, 1, 2, 6],
    [7, 0, 4, 6, 6, 4, 7],
    [9, 4, 0, 2, 9, 9, 2],
    [9, 6, 2, 0, 2, 7, 10],
    [1, 6, 9, 2, 0, 8, 8],
    [2, 4, 9, 7, 8, 0, 4],
    [6, 7, 2, 10, 8, 4, 0],
]

# Классы городов: каждый класс своим цветом
city_classes = [3, 1, 2, 3, 1, 2, 1]
# Class Requirements: {1: 1, 2: 2, 3: 2}
# 1: 'blue', 2: 'green', 3: 'red'
color_map = {1: 'blue', 2: 'green', 3: 'red'}

# Маршрут
min_route = (6, 2, 3, 4, 0, 5)

# Функция для рисования текущего состояния графа с подсвеченным путём
# Функция для рисования текущего состояния графа с подсвеченным путём
def draw_graph(G, pos, node_colors, path=None):
    # Рисуем все ребра чёрным цветом для основы
    nx.draw_networkx_edges(G, pos, edge_color='black', width=1)
    # Рисуем все узлы с их цветами в соответствии с классами
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
    # Рисуем метки на узлах
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold')
    # Если путь предоставлен, рисуем узлы пути с их цветами класса
    if path:
        # Создаем список цветов для узлов пути
        path_node_colors = [color_map[city_classes[node]] for node in path]
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=path_node_colors, node_size=1200, edgecolors='black', linewidths=2)
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    # Рисуем веса рёбер
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Создание графа на основе матрицы и классов
G = nx.Graph()

for i, row in enumerate(matrix):
    for j, x in enumerate(row):
        if x > 0:
            G.add_edge(i, j, weight=x)

# Цвета узлов на основе их классов
node_colors = [color_map[city_classes[n]] for n in G.nodes()]

# Расположение узлов
pos = nx.spring_layout(G)

# Последовательное отображение пути
for i in range(1, len(min_route) + 1):
    plt.figure(figsize=(12, 8))
    draw_graph(G, pos, node_colors, min_route[:i])
    plt.axis('off')
    plt.title(f"Step {i} of the path")
    plt.show()

    time.sleep(1)  # Пауза на 1 секунду
    clear_output(wait=True)  # Очистка