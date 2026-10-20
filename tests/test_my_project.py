import unittest
import sys
import os


from my_project import triangle_kind, process

class TestMyProject(unittest.TestCase):

    def test_equilateral_triangle(self):
        self.assertEqual(triangle_kind(5, 5, 5), "равносторонний")

    def test_isosceles_triangle_sides_a_b(self):
        self.assertEqual(triangle_kind(4, 4, 5), "равнобедренный")

    def test_isosceles_triangle_sides_b_c(self):
        self.assertEqual(triangle_kind(5, 4, 4), "равнобедренный")

    def test_isosceles_triangle_sides_a_c(self):
        self.assertEqual(triangle_kind(4, 5, 4), "равнобедренный")

    def test_scalene_triangle(self):
        self.assertEqual(triangle_kind(3, 4, 5), "разносторонний")

    def test_not_a_triangle_sum_equals(self):
        self.assertEqual(triangle_kind(2, 3, 5), "не треугольник")

    def test_not_a_triangle_sum_less(self):
        self.assertEqual(triangle_kind(0.002, 0.002, 0.005), "не треугольник")

    def test_process_valid_triangle(self):
        kind, coords = process("3", "4", "5")
        self.assertEqual(kind, "разносторонний")
        self.assertEqual(len(coords), 3)

    def test_process_non_numeric_data(self):
        kind, coords = process("abc", "4", "5")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_process_negative_numbers(self):
        kind, coords = process("-3", "4", "5")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_process_zero_side(self):
        kind, coords = process("0", "4", "5")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_process_existing_triangle_but_bad_sides(self):
        kind, coords = process("1", "1", "10")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

if __name__ == '__main__':
    unittest.main()