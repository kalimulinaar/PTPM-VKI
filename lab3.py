import sqlite3
from abc import ABC, abstractmethod


class TriangleCalculator:
    def calculate(self, a: float, b: float, c: float) -> str:
        eps = 1e-9
        if a + b - c <= eps or a + c - b <= eps or b + c - a <= eps:
            return "не треугольник"
        if abs(a - b) <= eps and abs(b - c) <= eps:
            return "равносторонний"
        if abs(a - b) <= eps or abs(b - c) <= eps or abs(a - c) <= eps:
            return "равнобедренный"
        return "разносторонний"


class TriangleDatabase:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Запрос в одну строку (без переносов)
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS triangles (a REAL, b REAL, c REAL, triangle_type TEXT, error_msg TEXT, PRIMARY KEY (a, b, c))")
        self.conn.commit()

    def get_result(self, a, b, c):
        self.cursor.execute("SELECT triangle_type, error_msg FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c))
        return self.cursor.fetchone()

    def add_result(self, a, b, c, triangle_type, error_msg=""):
        self.cursor.execute(
            "INSERT OR REPLACE INTO triangles (a, b, c, triangle_type, error_msg) VALUES (?, ?, ?, ?, ?)",
            (a, b, c, triangle_type, error_msg))
        self.conn.commit()

    def delete_result(self, a, b, c):
        self.cursor.execute("DELETE FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c))
        self.conn.commit()

class IUserInterface(ABC):
    @abstractmethod
    def get_input(self) -> tuple:
        pass


class IExternalService(ABC):
    @abstractmethod
    def send_data(self, message: str) -> bool:
        pass


class Controller:
    def __init__(self, ui: IUserInterface, db: TriangleDatabase, calc: TriangleCalculator,
                 email_service: IExternalService):
        self.ui = ui
        self.db = db
        self.calc = calc
        self.email_service = email_service

    def process_request(self) -> str:
        a, b, c = self.ui.get_input()

        db_result = self.db.get_result(a, b, c)

        if db_result:

            triangle_type = db_result[0]
            result_message = f"Из БД: {triangle_type}"
        else:
            triangle_type = self.calc.calculate(a, b, c)
            error_msg = "Стороны не образуют треугольник" if triangle_type == "не треугольник" else ""

            self.db.add_result(a, b, c, triangle_type, error_msg)
            result_message = f"Вычислено: {triangle_type}"

        self.email_service.send_data(result_message)

        # 4. Возвращаем результат
        return result_message