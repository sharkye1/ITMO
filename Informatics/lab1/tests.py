# tests.py
import unittest
from calculate import to_symmetric_base

class TestSymmetricBase(unittest.TestCase):
    def test_positive_9(self):
        self.assertEqual(to_symmetric_base(10, 9), "11")  # 10 = 1*9 + 1

    def test_negative_9(self):
        self.assertEqual(to_symmetric_base(-10, 9), "{^1}{^1}")  # -10 = -1*9 - 1

    def test_zero_5(self):
        self.assertEqual(to_symmetric_base(0, 5), "0")  # 0 в любой системе = 0

    def test_positive_3(self):
        self.assertEqual(to_symmetric_base(1, 3), "1")  # 1 в S3 = 1

    def test_large_positive_9(self):
        self.assertEqual(to_symmetric_base(25738, 9), "4{^1}3{^2}{^2}")  # Правильное разложение для 25738

    def test_large_negative_9(self):
        self.assertEqual(to_symmetric_base(-25738, 9), "{^4}1{^3}22")  # Как в примере

    def test_border_base_3(self):
        self.assertEqual(to_symmetric_base(4, 3), "11")  # 4 = 1*3^1 + 1*3^0

    def test_invalid_base_even(self):
        with self.assertRaises(ValueError):
            to_symmetric_base(5, 4)  # Чётное основание

    def test_invalid_base_non_int(self):
        with self.assertRaises(ValueError):
            to_symmetric_base(3, 3.5)  # Нецелочисленное основание

    def test_invalid_n_non_int(self):
        with self.assertRaises(ValueError):
            to_symmetric_base(3.5, 3)  # Нецелочисленное число

if __name__ == '__main__':
    unittest.main()