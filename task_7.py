import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from networkx.algorithms import bipartite
from PIL import Image
import general_functions
import os

x = ["x1", "x2", "x3", "x4", "x5", ""][::-1]
y = ["y1", "y2", "y3", "y4", "y5", "y6"][::-1]

edges_random_list = [
    "(x1,y2),(x1,y5),(x1,y6),(x2,y3),(x2,y4),(x2,y6),(x3,y1),(x3,y2),(x3,y4),(x3,y5),(x4,y1),(x4,y2),(x4,y5),(x5,y2),(x5,y3),(x5,y6)",
    "(x1,y5),(x1,y6),(x2,y1),(x2,y3),(x2,y4),(x3,y1),(x3,y2),(x3,y5),(x4,y2),(x4,y5),(x4,y6),(x5,y2),(x5,y4),(x5,y6)",
    "(x1,y5),(x1,y6),(x2,y3),(x2,y4),(x2,y5),(x3,y1),(x3,y2),(x3,y4),(x3,y5),(x4,y2),(x4,y3),(x4,y5),(x5,y2),(x5,y6)",
    "(x1,y5),(x1,y6),(x2,y3),(x2,y4),(x3,y2),(x3,y1),(x3,y5),(x4,y2),(x4,y3),(x4,y5),(x5,y1),(x5,y2),(x5,y6)",
    "(x1,y5),(x1,y6),(x2,y3),(x2,y4),(x3,y1),(x3,y2),(x3,y5),(x4,y2),(x4,y5),(x5,y2),(x5,y5),(x5,y6)",
    "(x1,y5),(x1,y6),(x2,y3),(x2,y4),(x3,y1),(x3,y2),(x3,y5),(x4,y2),(x4,y5),(x4,y6),(x5,y2),(x5,y4),(x5,y6)",
    "(x1,y6),(x1,y4),(x1,y1),(x2,y3),(x2,y5),(x2,y6),(x3,y1),(x3,y2),(x3,y6),(x4,y2),(x4,y5),(x5,y1),(x5,y2),(x5,y5)"]

DataFrame = pd.DataFrame(
    {'x': x,
     'y': y})


def create_gif():
    if not os.path.exists("gifs"):
        os.mkdir("gifs")
    global num_of_pictures
    pictures = []
    im = Image.open('0.png')
    pictures.append(Image.open('1.png'))

    im.save("gifs/out_task_7.gif", save_all=True, append_images=pictures, duration=1000, loop=0)


def create_image(_graph, image_name, pos):
    # colors = nx.get_edge_attributes(_graph, 'color').values()

    nx.draw(_graph, pos, edge_color="black", node_color='#cccccc', width=1, node_size=1000, with_labels=True)
    plt.gca().margins(0.10)  # отступы

    plt.savefig(image_name, dpi=600)
    plt.show()
    plt.close()


def create_graph():
    _graph = nx.Graph()
    _edges = list()  # создаём список для хранения рёбер

    edges_string = random.choice(edges_random_list)

    for edge in [edges_string[x:x + 8] for x in range(0, len(edges_string), 8)]:
        _edges.append([edge[1] + edge[2], edge[4] + edge[5]])  # преобразуем строку в список с рёбрами

    # print("Рёбра графа:", edges)

    _graph.add_nodes_from(DataFrame['x'], bipartite=0)  # связь
    _graph.add_nodes_from(DataFrame['y'], bipartite=1)
    _graph.remove_node("")

    for edge in _edges:
        _graph.add_edge(edge[0], edge[1], color='#cccccc')

    _pos = {node: [0, i] for i, node in enumerate(DataFrame['x'])}
    _pos.update({node: [1, i] for i, node in enumerate(DataFrame['y'])})  # двудольный граф

    return _graph, _pos, _edges


def find_perfect_matching(_graph, _edges):
    my_matching = bipartite.matching.hopcroft_karp_matching(_graph, y)  # находим совершенное паросочетание

    max_edges = list()

    _graph.clear_edges()

    for edge in _edges:
        if my_matching[edge[0]] == edge[1]:
            max_edges.append([edge[0], edge[1]])
            _graph.add_edge(edge[0], edge[1], color='black')

    # print("Совершенное паросочетание:", max_edges)


#####################################################################
def main():
    graph, pos, edges = create_graph()
    create_image(graph, "0.png", pos)  # весь граф

    find_perfect_matching(graph, edges)
    create_image(graph, "1.png", pos)  # совершенное паросочетание

    create_gif()
    general_functions.delete_pictures(2)
