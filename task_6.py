import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import copy
import general_functions


def create_position(edges, edges2):
    edges = edges + edges2
    global G, pos, edge_colors, edge_labels
    G = nx.Graph()
    for i in range(len(edges)):
        G.add_edges_from([edges[i][0]], weight=edges[i][1])

    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    pos = nx.circular_layout(G)


def show_graph(edges2, is_chord_or_cuts, title, colors):
    if is_chord_or_cuts:
        global edge_colors
        edges2_ = []
        for i in range(len(edges2)):
            edges2_.append(edges2[i][0])
        if colors:
            edge_colors = ['#DEB887' if edge in edges2_ else '#8B4513' for edge in G.edges()]
        else:
            edge_colors = ['#8B4513' if edge in edges2_ else '#DEB887' for edge in G.edges()]

    node_labels = {node: node for node in G.nodes()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    nx.draw(G, pos=pos, node_color='#DEB887', node_size=1500, edgecolors='#8B4513', edge_color=edge_colors)
    plt.title(title)
    plt.gca().margins(0.10)
    global num_of_pictures
    plt.savefig(f'{num_of_pictures}.png', dpi=400)
    num_of_pictures += 1
    plt.close()


def primsAlgorithm(vertices):
    adjacencyMatrix = [[0 for column in range(vertices)] for row in range(vertices)]
    mstMatrix = [[0 for column in range(vertices)] for row in range(vertices)]
    a=0
    for i in range(0, vertices):
        for j in range(i, vertices):
            if i == j:
                adjacencyMatrix[j][i] = adjacencyMatrix[i][j] = 0
            else:
                adjacencyMatrix[i][j] = int((randint(0, 20)))
                adjacencyMatrix[j][i] = adjacencyMatrix[i][j]

    positiveInf = float('inf')
    selectedVertices = [False for vertex in range(vertices)]
    chords_matrix = adjacencyMatrix
    while (False in selectedVertices):
        minimum = positiveInf
        start = 0
        end = 0
        for i in range(0, vertices):
            if selectedVertices[i]:
                for j in range(i, vertices):
                    if (not selectedVertices[j] and adjacencyMatrix[i][j] > 0):
                        if adjacencyMatrix[i][j] < minimum:
                            minimum = adjacencyMatrix[i][j]
                            start, end = i, j
        selectedVertices[end] = True
        mstMatrix[start][end] = minimum
        if minimum == positiveInf:
            mstMatrix[start][end] = 0
        mstMatrix[end][start] = mstMatrix[start][end]

        chords_matrix[start][end] = chords_matrix[end][start] = 0

    return mstMatrix, chords_matrix


def get_edges(adjacency_matrix):
    edges = []
    for i in range(len(adjacency_matrix)):
        for j in range(i, len(adjacency_matrix)):
            if adjacency_matrix[i][j] > 0:
                edges.append(((j, i), adjacency_matrix[i][j]))
                edges.append(((i, j), adjacency_matrix[i][j]))

    return edges


def get_cycles_cuts(edges, is_cuts):
    for i in range(len(edges)):
        for j in range(i, len(edges)):
            if edges[i][j] > 0:
                edges_ = copy.deepcopy(edges)
                edges_[i][j] = 0
                if is_cuts:
                    show_graph(get_edges(edges_), 1, 'cuts', 0)
                else:
                    show_graph(get_edges(edges_), 1, 'cycles', 1)


num_of_pictures = 0


def main():
    vertices = (input('Введите количество вершин (число не менее 2): '))
    while not general_functions.check_num(vertices):
        vertices = (input('Введите количество вершин (число не менее 2): '))
    vertices = int(vertices)

    A = primsAlgorithm(vertices)
    edges = get_edges(A[0])
    edges1 = get_edges(A[1])
    create_position(edges, edges1)
    show_graph(edges1, 1, 'spanning tree', 1)

    get_cycles_cuts(A[1], 0)
    get_cycles_cuts(A[0], 1)

    global num_of_pictures
    general_functions.create_gif(num_of_pictures, 6)
    general_functions.delete_pictures(num_of_pictures)

    num_of_pictures = 0

