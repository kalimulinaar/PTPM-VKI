import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from lab3 import Controller, TriangleCalculator, TriangleDatabase, IUserInterface, IExternalService


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.calc = TriangleCalculator()
        self.db = TriangleDatabase(":memory:")

        self.mock_ui = Mock(spec=IUserInterface)
        self.mock_email = Mock(spec=IExternalService)

        self.controller = Controller(self.mock_ui, self.db, self.calc, self.mock_email)

    def test_integration_controller_and_database(self):
        """ИНТЕГРАЦИОННЫЙ: Проверяем, что данные сохраняются в реальную БД и берутся из нее"""
        self.mock_ui.get_input.return_value = (3.0, 4.0, 5.0)

        result1 = self.controller.process_request()
        self.assertEqual(result1, "Вычислено: разносторонний")

        result2 = self.controller.process_request()
        self.assertEqual(result2, "Из БД: разносторонний")

    def test_integration_controller_and_calculator(self):
        """ИНТЕГРАЦИОННЫЙ: Проверяем, что контроллер правильно вызывает калькулятор для нового треугольника"""
        self.mock_ui.get_input.return_value = (5.0, 5.0, 5.0)
        result = self.controller.process_request()
        self.assertEqual(result, "Вычислено: равносторонний")

    def test_integration_controller_and_external_service(self):
        """ИНТЕГРАЦИОННЫЙ: Проверяем, что контроллер отправляет данные в сторонний сервис"""
        self.mock_ui.get_input.return_value = (3.0, 4.0, 5.0)
        self.controller.process_request()

        self.mock_email.send_data.assert_called_once_with("Вычислено: разносторонний")

    def test_database_delete_method(self):
        """Проверка метода удаления из БД (не дублирует ЛР2)"""
        self.db.add_result(1.0, 2.0, 3.0, "не треугольник")
        self.assertIsNotNone(self.db.get_result(1.0, 2.0, 3.0))

        self.db.delete_result(1.0, 2.0, 3.0)
        self.assertIsNone(self.db.get_result(1.0, 2.0, 3.0))

    def test_external_service_is_abstract(self):
        """Проверка, что нельзя создать экземпляр абстрактного класса (не дублирует ЛР2)"""
        with self.assertRaises(TypeError):
            IExternalService()


if __name__ == '__main__':
    unittest.main()