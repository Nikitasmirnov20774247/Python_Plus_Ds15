# ✔ Создайте класс прямоугольник.
# ✔ Класс должен принимать длину и ширину при создании
# экземпляра.
# ✔ У класса должно быть два метода, возвращающие периметр
# и площадь.
# ✔ Если при создании экземпляра передаётся только одна
# сторона, считаем что у нас квадрат.

# Решить задачи, которые не успели решить на семинаре.
# Возьмите любые 1-3 задачи из прошлых домашних заданий.
# Добавьте к ним логирование ошибок и полезной
# информации. Также реализуйте возможность запуска из
# командной строки с передачей параметров.


from pathlib import Path
import argparse
import logging


class ArgumentNotFound(TypeError):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"!! Аргумент не найден ({self.value}) !!"


class NonPositiveError(TypeError):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"!! Значение не может быть отрицательным ({self.value if self.value is not None else ''}) !!"


class NotZeroError(TypeError):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"!! Значение не может быть равным 0 ({self.value if self.value is not None else ''}) !!"


class Rectangle:
    def __init__(self, a, b=None):
        self.is_valid(a, b)
        self.a = a
        self.b = a if not b else b

    def get_perimeter(self):
        return 2 * (self.a + self.b)

    def get_area(self):
        return self.a * self.b

    def get_length(self):
        return self.a

    def get_width(self):
        return self.b

    def __str__(self):
        if self.a == self.b:
            rstr = f"квадрат со сторонами {self.a} и {self.b}"
        else:
            rstr = f"прямоугольник со сторонами {self.a} и {self.b}"
        return rstr

    @staticmethod
    def is_valid(a, b):
        if a is None:
            raise ArgumentNotFound(f"{a = }")
        if (a is not None and a < 0) or (b is not None and b < 0):
            raise NonPositiveError(f"{f'{a = }' if a < 0 else f'{b = }'}")
        if (a is not None and a == 0) or (b is not None and b == 0):
            raise NotZeroError(f"{f'{a = }' if a == 0 else f'{b = }'}")


def get_logger(filename=f'logs/Ds1_1.log'):
    DIR_LOGS = Path.cwd() / 'logs'
    if not DIR_LOGS.is_dir():
        DIR_LOGS.mkdir()

    FORMAT_MSG = "{asctime} {levelname} {funcName}: {msg}"
    logging.basicConfig(filename=filename, filemode='a', encoding='utf-8',
                        level=logging.DEBUG, style='{', format=FORMAT_MSG)
    
    return logging.getLogger()


if __name__ == '__main__':
    logger = get_logger()
    parse = argparse.ArgumentParser(description="Получение площади и длины прямоугольника по указанным размерам")
    parse.add_argument('-a', type=float, metavar='length', nargs='?', default=10)
    parse.add_argument('-b', type=float, metavar='width', nargs='?', default=None)
    args = parse.parse_args()
    
    try:
        r1 = Rectangle(a=args.a, b=args.b)
        logger.info(f'Cоздан: {str(r1)}')
        area = r1.get_area()
        logger.info(f'Получен: {area = }')
        perimeter = r1.get_perimeter()
        logger.info(f'Получен: {perimeter = }')
        print(f"Результат: {str(r1)}\nПлощадь: {area}\nПериметр: {perimeter}")
    except (ArgumentNotFound, NonPositiveError, NotZeroError) as err:
        print(err)
        logger.error(err)
