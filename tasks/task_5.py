import copy
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from tasks import general_functions


def graph_generation(num_vertices):
    """!@brief
        Функция для генерации ребер графа.

        @arg edges [list] — список для хранения ребер.

        @param int $num_vertices — количество вершин.

        @retval list $edges — cписок соединенных вершин.
        """

    edges = []
    for i in range(num_vertices):
        for j in range(i, num_vertices):
            edges.append((i, randint(i+1, num_vertices)))

    return edges


def create_matrix(vertices, edges):
    """!@brief
        Функция для создания матрицы смежности.

        @arg adjacency_matrix [list] — матрица смежности.

        @param int $vertices — количество вершин.
        @param list $edges — cписок соединенных вершин.

        @retval list $adjacency_matrix — матрица смежности.
        """

    adjacency_matrix = [[0 for column in range(vertices)] for row in range(vertices)]

    for i in range(vertices):
        for j in range(i, vertices):
            for k in range(len(edges)):
                if j == edges[k][0]:
                    adjacency_matrix[j][edges[k][1]] = 1
                    adjacency_matrix[edges[k][1]][j] = adjacency_matrix[j][edges[k][1]]

    return adjacency_matrix


def spanning_tree_and_chords(adjacency_matrix, vertices):
    """!@brief
        Функция для поиска каркаса и хорд.

        @arg st_matrix [list] — матрица смежности, содержащая только каркас.
        @arg chords_matrix [list] — матрица смежности, содержащая только хорды.
        @arg selected_vertices [list] — список, показывающий связи, которые еще не добавлены в матрицу смежности.

        @param list $adjacency_matrix — матрица смежности.
        @param int $vertices — количество вершин.

        @retval list $st_matrix — матрица смежности, содержащая только каркас.
        @retval list $chords_matrix — матрица смежности, содержащая только хорды.
        """

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
    """!@brief
        Функция для преобразования матрицы смежности в список соединенных вершин.

        @arg edges [list] — список для хранения ребер.

        @param list $adjacency_matrix — матрица смежности.

        @retval list $edges — cписок соединенных вершин.
        """

    edges = []
    for i in range(len(adjacency_matrix)):
        for j in range(i, len(adjacency_matrix)):
            if adjacency_matrix[i][j] == 1:
                edges.append((i, j))
                edges.append((j, i))

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
                    show_graph(get_edges(edges_), 1, 'cuts', 1)
                else:
                    show_graph(get_edges(edges_), 1, 'cycles', 0)


def create_position(edges):
    """!@brief
        Функция для построения положения графа на полотне.

        @arg G [Graph] — объект класса Graph.
        @arg position [dict] — координаты вершин графа.
        @arg edge_colors [string] — цвет ребер.

        @param list $edges — список соединенных вершин.
        """

    global G, position, edge_colors
    G = nx.Graph()
    G.add_edges_from(edges)
    position = nx.circular_layout(G)
    edge_colors = 'black'


def show_graph(edges, is_chord_or_cuts, title, is_cuts):
    """!@brief
        Функция для отрисовки графа на полотне.

        @arg node_labels [list] — список номеров вершин.

        @param list $edges — список соединенных вершин.
        @param bool $is_chord_or_cuts — флаг для определения того, что передано в функцию (полный граф, каркас, ФСЦ или разрезы).
        @param string $title — текстовое обозначение того, что будет отрисовано.
        @param bool $is_cuts — флаг для определения того, что передается в функцию (ФСЦ или разрезы).
        """

    if is_chord_or_cuts:
        global edge_colors
        if is_cuts:
            edge_colors = ['black' if edge in edges else '#BCBEC0' for edge in G.edges()]
        else:
            edge_colors = ['#BCBEC0' if edge in edges else 'black' for edge in G.edges()]

    node_labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, position, labels=node_labels, font_size=12)
    nx.draw(G, pos=position, node_color='#ffd4fb', node_size=800, edge_color=edge_colors)
    plt.title(title)
    plt.gca().margins(0.10)

    global num_of_pictures
    plt.savefig(f'{num_of_pictures}.png', dpi=400)
    num_of_pictures += 1

    plt.close()


num_of_pictures = 0


def main():
    """!@brief
        Основная функция, необходимая для решения задачи.
        На основе введенного пользователем числа вершин генерирует ребра для ненагруженного графа, ищет его каркас, фундаментальную систему циклов и разрезы.

        @author Васюткин А.О.
        @date Март, 2022
        """

    vertices = (input('Введите количество вершин (число от 2 до 15):'))
    while not general_functions.check_num(vertices):
        vertices = (input('Введите количество вершин (число от 2 до 15): '))
    vertices = int(vertices)

    edges = graph_generation(vertices-1)
    adjacency_matrix = create_matrix(vertices, edges)

    edges = get_edges(adjacency_matrix)
    create_position(edges)
    show_graph(edges, 0, 'graph', 0)

    tree = spanning_tree_and_chords(adjacency_matrix, vertices)
    show_graph(get_edges(tree[1]), 1, 'spanning tree', 0)

    get_cycles_cuts(tree[1], 0)
    get_cycles_cuts(tree[0], 1)

    global num_of_pictures
    general_functions.create_gif(num_of_pictures, 5)
    general_functions.delete_pictures(num_of_pictures)

    num_of_pictures = 0
