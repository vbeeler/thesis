import unittest
from src.general import hook_lengths, integer_partitions, nested_product, \
        deg_of_irr_rep

class TestGeneralFunctions(unittest.TestCase):

    def test_hook_lengths(self):
        self.assertEqual(hook_lengths([5, 4, 3, 2, 1]), [[1], [3, 1], \
                [5, 3, 1], [7, 5, 3, 1], [9, 7, 5, 3, 1]])
        self.assertEqual(hook_lengths([5, 3, 3]), [[3, 2, 1], [4, 3, 2], \
                [7, 6, 5, 2, 1]])
        self.assertEqual(hook_lengths([6]), [[6, 5, 4, 3, 2, 1]])
        self.assertEqual(hook_lengths([1, 1, 1, 1]), [[1], [2], [3], [4]])
        self.assertEqual(hook_lengths([]), [[]])
        self.assertEqual(hook_lengths([6, 5, 4, 1]), [[1], [5, 3, 2, 1], \
                [7, 5, 4, 3, 1], [9, 7, 6, 5, 3, 1]])
        self.assertEqual(hook_lengths([5, 2, 2, 1]), [[1], [3, 1], [4, 2], \
                [8, 6, 3, 2, 1]])
        self.assertEqual(hook_lengths([4, 3, 1, 1, 1]), [[1], [2], [3], \
                [6, 2, 1], [8, 4, 3, 1]])
        self.assertEqual(hook_lengths([7, 5, 4, 4, 2, 1, 1]), [[1], [2], \
                [4, 1], [7, 4, 2, 1], [8, 5, 3, 2], [10, 7, 5, 4, 1], \
                [13, 10, 8, 7, 4, 2, 1]])
        self.assertEqual(hook_lengths([3, 2]), [[2, 1], [4, 3, 1]])
        self.assertEqual(hook_lengths([5, 2, 1, 1, 1]), [[1], [2], [3], \
                [5, 1], [9, 5, 3, 2, 1]])

    def test_integer_partitions(self):
        self.assertEqual(integer_partitions(1), [[1]])
        self.assertEqual(integer_partitions(2), [[2], [1, 1]])
        self.assertEqual(integer_partitions(3), [[3], [2, 1], [1, 1, 1]])
        self.assertEqual(integer_partitions(4), [[4], [3, 1], [2, 2], \
                [2, 1, 1], [1, 1, 1, 1]])
        self.assertEqual(integer_partitions(5), [[5], [4, 1], [3, 2], \
                [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]])
        self.assertEqual(integer_partitions(6), [[6], [5, 1], [4, 2], \
                [4, 1, 1], [3, 3], [3, 2, 1], [3, 1, 1, 1], [2, 2, 2], \
                [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]])
        self.assertEqual(integer_partitions(10), [[10], [9, 1], [8, 2], \
                [8, 1, 1], [7, 3], [7, 2, 1], [7, 1, 1, 1], [6, 4], [6, 3, 1], \
                [6, 2, 2], [6, 2, 1, 1], [6, 1, 1, 1, 1], [5, 5], [5, 4, 1], \
                [5, 3, 2], [5, 3, 1, 1], [5, 2, 2, 1], [5, 2, 1, 1, 1], \
                [5, 1, 1, 1, 1, 1], [4, 4, 2], [4, 4, 1, 1], [4, 3, 3], \
                [4, 3, 2, 1], [4, 3, 1, 1, 1], [4, 2, 2, 2], \
                [4, 2, 2, 1, 1], [4, 2, 1, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1], \
                [3, 3, 3, 1], [3, 3, 2, 2], [3, 3, 2, 1, 1], \
                [3, 3, 1, 1, 1, 1], [3, 2, 2, 2, 1], [3, 2, 2, 1, 1, 1], \
                [3, 2, 1, 1, 1, 1, 1], [3, 1, 1, 1, 1, 1, 1, 1], \
                [2, 2, 2, 2, 2], [2, 2, 2, 2, 1, 1], [2, 2, 2, 1, 1, 1, 1], \
                [2, 2, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

    def test_nested_product(self):
        self.assertEqual(nested_product([[3, 2, 1], [5, 2, 1]]), 60)
        self.assertEqual(nested_product([[24, 5, 1]]), 120)
        self.assertEqual(nested_product([[1, 3, 8, 1], [2, 4, 1]]), 192)

    def test_deg_of_irr_rep(self):
        self.assertEqual(deg_of_irr_rep([4]), 1)
        self.assertEqual(deg_of_irr_rep([3, 1]), 3)
        self.assertEqual(deg_of_irr_rep([2, 2]), 2)
        self.assertEqual(deg_of_irr_rep([2, 1, 1]), 3)
        self.assertEqual(deg_of_irr_rep([1, 1, 1, 1]), 1)
        # left off testing here - pick larger integer partitions to test

if __name__ == '__main__':
    unittest.main()
