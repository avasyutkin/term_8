import copy
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from PIL import Image
import os


def graph_generation(num_vertices):
    edges = []
    for i in range(num_vertices):
        for j in range(i, num_vertices):
            edges.append((i, randint(i+1, num_vertices)))

    return edges


def create_matrix(vertices, edges):
    adjacency_matrix = [[0 for column in range(vertices)] for row in range(vertices)]

    for i in range(vertices):
        for j in range(i, vertices):
            for k in range(len(edges)):
                if j == edges[k][0]:
                    adjacency_matrix[j][edges[k][1]] = 1
                    adjacency_matrix[edges[k][1]][j] = adjacency_matrix[j][edges[k][1]]

    return adjacency_matrix


def spanning_tree_and_chords(adjacency_matrix, vertices):
    st_matrix = [[0 for column in range(vertices)] for row in range(vertices)]
    selected_vertices = [False for vertex in range(vertices)]
    chords_matrix = adjacency_matrix
    while False in selected_vertices:
        start = end = 0

        for i in range(vertices):
            if selected_vertices[i]:
                for j in range(vertices):
                    if not selected_vertices[j] and adjacency_matrix[i][j] == 1:
                        start, end = i, j

        selected_vertices[end] = True

        st_matrix[start][end], st_matrix[end][start] = adjacency_matrix[start][end], adjacency_matrix[start][end]
        chords_matrix[start][end] = chords_matrix[end][start] = 0

    return st_matrix, chords_matrix


def get_edges(adjacency_matrix):
    edges = []
    for i in range(len(adjacency_matrix)):
        for j in range(i, len(adjacency_matrix)):
            if adjacency_matrix[i][j] == 1:
                edges.append((i, j))
                edges.append((j, i))

    return edges


def get_cycles_cuts(edges, is_cuts):
    for i in range(len(edges)):
        for j in range(i, len(edges)):
            if edges[i][j] > 0:
                edges_ = copy.deepcopy(edges)
                edges_[i][j] = 0
                if is_cuts:
                    show_graph(get_edges(edges_), 1, 'cuts')
                else:
                    show_graph(get_edges(edges_), 1, 'cycles')


def create_position(edges):
    global G, position, edge_colors
    G = nx.Graph()
    G.add_edges_from(edges)
    position = nx.circular_layout(G)
    edge_colors = 'black'


def show_graph(edges, is_chord_or_cuts, title):
    if is_chord_or_cuts:
        global edge_colors
        edge_colors = ['#BCBEC0' if edge in edges else 'black' for edge in G.edges()]


    node_labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, position, labels=node_labels, font_size=12)
    nx.draw(G, pos=position, node_color='#ffd4fb', node_size=800, edge_color=edge_colors)
    plt.title(title)
    plt.gca().margins(0.10)
    global num_of_pictures
    plt.savefig(f'{num_of_pictures}.png', dpi=400)
    num_of_pictures += 1

    #plt.show()


def create_gif():
    pictures = []
    im = Image.open('0.png')
    for picture in range(num_of_pictures):
        pictures.append(Image.open(f'{picture}.png'))

    im.save("out.gif", save_all=True, append_images=pictures, duration=2000, loop=0)


def delete_pictures():
    for picture in range(num_of_pictures):
        os.remove(f'{picture}.png')


num_of_pictures = 0
vertices = int(input('Введите количество вершин: '))

edges = graph_generation(vertices-1)
adjacency_matrix = create_matrix(vertices, edges)

edges = get_edges(adjacency_matrix)
#print(get_edges(adjacency_matrix))
create_position(edges)
show_graph(edges, 0, 'graph')

tree = spanning_tree_and_chords(adjacency_matrix, vertices)
#print(get_edges(tree[0]), get_edges(tree[1]))
show_graph(get_edges(tree[1]), 1, 'spanning tree')

get_cycles_cuts(tree[1], 0)
get_cycles_cuts(tree[0], 1)

create_gif()
delete_pictures()