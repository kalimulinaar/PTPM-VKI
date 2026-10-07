import logging
import math

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
    ],
)


def triangle_kind(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"
    if a == b == c:
        return "равносторонний"
    if a == b or b == c or a == c:
        return "равнобедренный"
    return "разносторонний"


def triangle_vertices(a, b, c):
    ax, ay = 0, 0
    bx, by = a, 0

    cx = (a * a + b * b - c * c) / (2 * a)
    cy = math.sqrt(b * b - cx * cx)

    xs = [ax, bx, cx]
    ys = [ay, by, cy]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    w = max_x - min_x
    h = max_y - min_y
    scale = 80 / max(w, h)

    def to_px(x, y):
        px = int(10 + (x - min_x) * scale)
        py = int(90 - (y - min_y) * scale)
        return (px, py)

    return [to_px(ax, ay), to_px(bx, by), to_px(cx, cy)]


def process(a_raw, b_raw, c_raw):
    try:
        a = float(a_raw)
        b = float(b_raw)
        c = float(c_raw)
    except ValueError:
        logging.warning("Нечисловые данные: %r %r %r", a_raw, b_raw, c_raw)
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logging.warning("Некорректные числа: %s %s %s", a, b, c)
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    kind = triangle_kind(a, b, c)

    if kind == "не треугольник":
        logging.info("Не треугольник: %s %s %s", a, b, c)
        return kind, [(-1, -1), (-1, -1), (-1, -1)]

    return kind, triangle_vertices(a, b, c)


def main():
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")
    print("Введите три стороны треугольника (пустая строка — выход).")

    while True:
        a = input("A: ")
        if a.strip() == "":
            logging.info("Выход по пустой строке")
            break
        b = input("B: ")
        c = input("C: ")

        kind, vertices = process(a, b, c)
        logging.info("Тип: %s, координаты: %s", kind, vertices)
        print(f"Тип: {kind}")
        print(f"Координаты: {vertices}")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()