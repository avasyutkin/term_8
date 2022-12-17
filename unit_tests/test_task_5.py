import unittest
import tasks.task_5 as task_5

test_data = {
    'vertices': 5,
    'edges': [(0, 1), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
    'spanning_tree': [(0, 1), (1, 0), (0, 3), (3, 0), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)]
  }


class TestTask5(unittest.TestCase):
    def test_task_5(self):
        spanning_tree = task_5.get_edges(task_5.spanning_tree_and_chords(task_5.create_matrix(test_data['vertices'], test_data['edges']), test_data['vertices'])[1])
        self.assertEqual(spanning_tree, test_data['spanning_tree'])
