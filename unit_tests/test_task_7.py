import unittest
import tasks.task_7 as task_7

test_data = {
    'edges': '(x1,y5),(x1,y6),(x2,y3),(x2,y4),(x2,y5),(x3,y1),(x3,y2),(x3,y4),(x3,y5),(x4,y2),(x4,y3),(x4,y5),(x5,y2),(x5,y6)',
    'perfect_matching': [[['x1', 'y6'], ['x2', 'y4'], ['x3', 'y1'], ['x4', 'y3'], ['x5', 'y2']],
                         [['x1', 'y5'], ['x2', 'y4'], ['x3', 'y2'], ['x4', 'y3'], ['x5', 'y6']],
                         [['x1', 'y5'], ['x2', 'y3'], ['x3', 'y1'], ['x4', 'y2'], ['x5', 'y6']],
                         [['x1', 'y6'], ['x2', 'y4'], ['x3', 'y1'], ['x4', 'y5'], ['x5', 'y2']],
                         [['x1', 'y5'], ['x2', 'y4'], ['x3', 'y1'], ['x4', 'y2'], ['x5', 'y6']],
                         [['x1', 'y6'], ['x2', 'y3'], ['x3', 'y4'], ['x4', 'y5'], ['x5', 'y2']],
                         [['x1', 'y5'], ['x2', 'y4'], ['x3', 'y1'], ['x4', 'y3'], ['x5', 'y6']],
                         [['x1', 'y6'], ['x2', 'y3'], ['x3', 'y1'], ['x4', 'y5'], ['x5', 'y2']],
                         [['x1', 'y5'], ['x2', 'y3'], ['x3', 'y4'], ['x4', 'y2'], ['x5', 'y6']],
                         [['x1', 'y6'], ['x2', 'y5'], ['x3', 'y1'], ['x4', 'y3'], ['x5', 'y2']],
                         [['x1', 'y6'], ['x2', 'y5'], ['x3', 'y4'], ['x4', 'y3'], ['x5', 'y2']],
                         [['x1', 'y6'], ['x2', 'y4'], ['x3', 'y5'], ['x4', 'y3'], ['x5', 'y2']]]
}


class TestTask5(unittest.TestCase):
    def test_task_5(self):
        graph, pos, edges = task_7.create_graph(test_data['edges'])
        perfect_matching = task_7.find_perfect_matching(graph, edges)
        self.assertIn(perfect_matching, test_data['perfect_matching'])