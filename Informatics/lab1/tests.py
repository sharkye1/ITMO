import unittest
from Informatics.lab1.calculate import to_symmetric_base

class TestSymmetricBase(unittest.TestCase):
    def test_positive_9(self):
        self.assertEqual(to_symmetric_base(10, 9), "11")
    
    def test_negative_9(self):
        self.assertEqual(to_symmetric_base(-10, 9), "{^1}1{^1}")  # уточни ожидаемое

    def test_zero_9(self):
        self.assertEqual(to_symmetric_base(0, 9), "0")

    def test_positive_3(self):
        self.assertEqual(to_symmetric_base(4, 3), "11")

    def test_negative_3(self):
        self.assertEqual(to_symmetric_base(-4, 3), "{^1}{^1}")

    def test_invalid_base_even(self):
        self.assertRaises(ValueError, to_symmetric_base, 5, 4)

    def test_invalid_base_too_small(self):
        self.assertRaises(ValueError, to_symmetric_base, 2, 1)

    def test_invalid_base_negative(self):
        self.assertRaises(ValueError, to_symmetric_base, 3, -3)

    def test_invalid_base_non_int(self):
        self.assertRaises(ValueError, to_symmetric_base, 3, 3.5)

    def test_invalid_n_non_int(self):
        self.assertRaises(ValueError, to_symmetric_base, 3.5, 3)

if __name__ == '__main__':
    unittest.main()