import unittest
import sys
import os



from delivery_service import calculate_delivery_cost

class TestDeliveryService(unittest.TestCase):

    def test_valid_standard_delivery(self):
        cost, date = calculate_delivery_cost(3.0, 100, "обычный", False)
        # 200 + (100 * 5) = 700
        self.assertEqual(cost, 700)

    def test_invalid_weight_too_large(self):
        cost, date = calculate_delivery_cost(51.0, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_weight_too_small(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_distance_too_long(self):
        cost, date = calculate_delivery_cost(10.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(10.0, 100, "секретный")
        self.assertEqual(cost, -1)

    def test_fragile_package_cost(self):
        # База 200 + 500 + 300 (хрупкий) = 1000
        cost, _ = calculate_delivery_cost(3.0, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)

    def test_dangerous_package_cost(self):
        # 200 + 500 + 1000 (опасный) = 1700
        cost, _ = calculate_delivery_cost(3.0, 100, "опасный", False)
        self.assertEqual(cost, 1700)

    def test_weight_boundary_20(self):
        # Вес 20.0 должен получить коэффициент 1.5
        # 700 * 1.5 = 1050
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    def test_express_delivery_is_more_expensive(self):
        cost_normal, _ = calculate_delivery_cost(3.0, 100, "обычный", False)
        cost_express, _ = calculate_delivery_cost(3.0, 100, "обычный", True)
        self.assertGreater(cost_express, cost_normal)

    def test_express_delivery_days_not_zero(self):
        _, date = calculate_delivery_cost(3.0, 500, "обычный", True)
        self.assertNotEqual(date, "2026-09-03")

    def test_weight_5kg_gets_coefficient(self):
        cost_4_9, _ = calculate_delivery_cost(4.9, 100, "обычный", False)
        cost_5_0, _ = calculate_delivery_cost(5.0, 100, "обычный", False)
        self.assertGreater(cost_5_0, cost_4_9)

    def test_delivery_days_calculation(self):
        _, date = calculate_delivery_cost(3.0, 1500, "обычный", False)
        self.assertNotEqual(date, "2026-09-03")


if __name__ == '__main__':
    unittest.main()