import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import copy
from tasks import general_functions


def create_position(edges, edges2):
    """!@brief
        Функция для построения положения графа на полотне.

        @arg G [Graph] — объект класса Graph.
        @arg pos [dict] — координаты вершин графа.
        @arg edge_colors [string] — цвет ребер.
        @arg edge_labels [dict] — список весов ребер.

        @param list $edges — список соединенных вершин (каркас).
        @param list $edges2 — список соединенных вершин (хорды).
        """
    edges = edges + edges2
    global G, pos, edge_colors, edge_labels
    G = nx.Graph()
    for i in range(len(edges)):
        G.add_edges_from([edges[i][0]], weight=edges[i][1])

    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    pos = nx.circular_layout(G)


def show_graph(edges2, is_chord_or_cuts, title, colors):
    """!@brief
        Функция для отрисовки графа на полотне.

        @arg node_labels [list] — список номеров вершин.

        @param list $edges2 — список соединенных вершин.
        @param bool $is_chord_or_cuts — флаг для определения того, что передано в функцию (каркас или ФСЦ/разрезы).
        @param string $title — текстовое обозначение того, что будет отрисовано.
        @param bool $colors — флаг для определения того, что передается в функцию (ФСЦ или разрезы).
        """
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


def create_matrix(vertices):
    """!@brief
        Функция для генерации ребер, их веса и создания матрицы смежности.

        @arg adjacencyMatrix [list] — матрица смежности.

        @param int $vertices — количество вершин.

        @retval list $adjacencyMatrix — матрица смежности.
        """
    adjacencyMatrix = [[0 for column in range(vertices)] for row in range(vertices)]
    for i in range(0, vertices):
        for j in range(i, vertices):
            if i == j:
                adjacencyMatrix[j][i] = adjacencyMatrix[i][j] = 0
            else:
                adjacencyMatrix[i][j] = int((randint(0, 20)))
                adjacencyMatrix[j][i] = adjacencyMatrix[i][j]

    return adjacencyMatrix


def spanning_tree_and_chords(adjacencyMatrix, vertices):
    """!@brief
        Функция для поиска каркаса и хорд.

        @arg mstMatrix [list] — матрица смежности, содержащая только каркас.
        @arg chords_matrix [list] — матрица смежности, содержащая только хорды.
        @arg selectedVertices [list] — список, показывающий связи, которые еще не добавлены в матрицу смежности.
        @arg positiveInf [float] — большое число, чтобы сравнивать с другими числами для нахождение минимального числа.
        @arg count [int] — счетчик для нейтрализации редкого зависания при поиске каркаса.

        @param list $adjacencyMatrix — матрица смежности.
        @param int $vertices — количество вершин.

        @retval list $mstMatrix — матрица смежности, содержащая только каркас.
        @retval list $chords_matrix — матрица смежности, содержащая только хорды.
        """
    mstMatrix = [[0 for column in range(vertices)] for row in range(vertices)]
    positiveInf = float('inf')
    selectedVertices = [False for vertex in range(vertices)]
    chords_matrix = adjacencyMatrix
    count = 0
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
        count += 1
        if count > 100:
            print("Произошла ошибка.")
            break

    return mstMatrix, chords_matrix


def get_edges(adjacency_matrix):
    """!@brief
        Функция для преобразования матрицы смежности в список соединенных вершин.

        @arg edges [list] — список для хранения ребер.

        @param list $adjacency_matrix — матрица смежности.

        @retval list $edges — cписок соединенных вершин.
        """
    edges = []
    for i in range(len(adjacency_matrix)):
        for j in range(i, len(adjacency_matrix)):
            if adjacency_matrix[i][j] > 0:
                edges.append(((j, i), adjacency_matrix[i][j]))
                edges.append(((i, j), adjacency_matrix[i][j]))

    return edges


def get_cycles_cuts(edges, is_cuts):
    """!@brief
        Промежуточная функция передачи фундаментальной системы циклов и разрезов графа в функцию отрисовки графа.

        @param bool $is_cuts — флаг для определения того, что необходимо найти (ФСЦ или разрезы).
        @param list $edges — матрица смежности.
        """
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
    """!@brief
        Основная функция.
        На основе введенного пользователем числа вершин случайным образом генерирует ребра и веса для нагруженного графа, ищет его каркас, фундаментальную систему циклов и разрезы.

        @author Каваллини Э.Д.
        @date Март, 2022
    """

    vertices = (input('Введите количество вершин (число от 2 до 15):'))
    while not general_functions.check_num(vertices):
        vertices = (input('Введите количество вершин (число от 2 до 15):'))
    vertices = int(vertices)

    matrix = create_matrix(vertices)

    tree = spanning_tree_and_chords(matrix, vertices)

    edges = get_edges(tree[0])
    edges1 = get_edges(tree[1])
    create_position(edges, edges1)
    show_graph(edges1, 1, 'spanning tree', 1)

    get_cycles_cuts(tree[1], 0)
    get_cycles_cuts(tree[0], 1)

    global num_of_pictures
    general_functions.create_gif(num_of_pictures, 6)
    general_functions.delete_pictures(num_of_pictures)

    num_of_pictures = 0

