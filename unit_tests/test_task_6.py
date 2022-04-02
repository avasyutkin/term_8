import unittest
import tasks.task_6 as task_6

test_data = {
    'vertices': 6,
    'edges': [[0, 8, 10, 4, 12, 2], [8, 0, 14, 11, 20, 19], [10, 14, 0, 1, 14, 10], [4, 11, 1, 0, 7, 15], [12, 20, 14, 7, 0, 2], [2, 19, 10, 15, 2, 0]],
    'spanning_tree': [((1, 0), 8), ((0, 1), 8), ((2, 0), 10), ((0, 2), 10), ((3, 0), 4), ((0, 3), 4), ((5, 0), 2), ((0, 5), 2), ((4, 3), 7), ((3, 4), 7)]
  }


class TestTask5(unittest.TestCase):
    def test_task_5(self):
        spanning_tree = task_6.get_edges(task_6.spanning_tree_and_chords(test_data['edges'], test_data['vertices'])[0])
        self.assertEqual(spanning_tree, test_data['spanning_tree'])




