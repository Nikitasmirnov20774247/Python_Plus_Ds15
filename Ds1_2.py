# Добавьте ко всем задачам с семинара строки документации и методы вывода
# информации на печать.
# Создайте класс Матрица. Добавьте методы для:
# * вывода на печать,
# * сравнения,
# * сложения,
# * *умножения матриц

# Решить задачи, которые не успели решить на семинаре.
# Возьмите любые 1-3 задачи из прошлых домашних заданий.
# Добавьте к ним логирование ошибок и полезной
# информации. Также реализуйте возможность запуска из
# командной строки с передачей параметров.


from pathlib import Path
import argparse
import logging


class ValFormatMatrixError(Exception):
    def __init__(self, operation, matrix=None, other_matrix = None):
        self.operation = operation
        self.matrix = matrix
        self.other_matrix = other_matrix

    def __str__(self):
        imposter_matrix = self.matrix
        if self.operation == '+':
            return f"!! Матрицы разных размеров невозможно сложить: m1 = {self.matrix if self.matrix is not None else ''}, m2 = {self.other_matrix if self.other_matrix is not None else ''}!!"
        elif self.operation == '*':
            return f"!! Данные матрицы невозможно перемножить: m1 = {self.matrix if self.matrix is not None else ''}, m2 = {self.other_matrix if self.other_matrix is not None else ''}!!"
        elif self.operation == 'S':
            return f"!! Операции сложения и умножения матриц возможны, если они полностью заполнены числами: {f'{self.matrix}' if self.matrix is not None else ''}!!"
        else:
            return f"!! Данная матрица не возможна: {f'{imposter_matrix = }' if self.matrix is not None else ''}!!"


class Matrix:
    '''
    Класс Matrix
    Данный класс создаёт экземпляр матрицы по полученному массиву, если переданный массив верен.
    '''


    def __init__(self, matrix):
        '''
        Метод __init__
        Инициализация аргументов, а также проверка
        на возможность существования матрицы.
        '''
        if type(matrix) != list:
            raise ValFormatMatrixError('!=', str(matrix))
        self.conversion_to_int(matrix)
        try:
            if len(set(map(len, matrix))) != 1:
                raise ValFormatMatrixError('!=', str(matrix))
        except:
            raise ValFormatMatrixError('!=', str(matrix))
        self.count_row = len(matrix)
        self.count_col = len(matrix[0])
        self.matrix = matrix


    def __add__(self, other):
        '''
        Метод __add__
        Переопределенный метод для поэлементного сложения матриц.
        Выполняет сложение двух экземпляров класса, если
        у двух слагаемых одинаковый размер (число столбцов и строк).
        '''
        self.check_num(self.matrix)
        self.check_num(other.matrix)
        if self.count_row != other.count_row or self.count_col != other.count_col:
            raise ValFormatMatrixError('+', str(self.matrix), str(other.matrix))
        new_matrix = []

        for x in range(self.count_row):
            row = []
            for y in range(self.count_col):
                row.append(self.matrix[x][y] + other.matrix[x][y])
            new_matrix.append(row)

        return Matrix(new_matrix)


    def __mul__(self, other):
        '''
        Метод __mul__
        Переопределенный метод для умножения матриц.
        Выполняет умножение двух экземпляров класса, если
        число столбцов в первом сомножителе равно числу строк во втором.
        '''
        self.check_num(self.matrix)
        self.check_num(other.matrix)
        if self.count_col != other.count_row:
            raise ValFormatMatrixError('*', str(self.matrix), str(other.matrix))
        new_matrix = []

        for x in range(self.count_row):
            row = []
            for y in range(other.count_col):
                res = 0
                for z in range(self.count_col):
                    res += self.matrix[x][z] * other.matrix[z][y]
                row.append(res)
            new_matrix.append(row)

        return Matrix(new_matrix)


    def __eq__(self, other):
        '''
        Метод __eq__
        Переопределённый метод для сравнения матриц.
        Матрицы могут быть равны когда равны их длины и каждый элемент.
        '''
        return self.matrix == other.matrix


    def __str__(self):
        '''
        Метод __str__
        Переопределенный метод для вывода матрицы.
        "Красивый" вывод экземпляра матрицы.
        '''
        s = '['
        for i in range(len(self.matrix)):
            s += str(self.matrix[i])
            if i != len(self.matrix) - 1:
                s += ', '
        s += ']'

        return s


    @staticmethod
    def conversion_to_int(matrix):
        for n, i in enumerate(matrix):
            for k, j in enumerate(i):
                try:
                    matrix[n][k] = int(j)
                except:
                    continue


    @staticmethod
    def check_num(matrix):
        for i in matrix:
            for j in i:
                if type(j) != float and type(j) != int:
                    raise ValFormatMatrixError('S', str(matrix))
                


def get_logger(filename=f'logs/Ds1_2.log'):
    DIR_LOGS = Path.cwd() / 'logs'
    if not DIR_LOGS.is_dir():
        DIR_LOGS.mkdir()

    FORMAT_MSG = "{asctime} {levelname} {funcName}: {msg}"
    logging.basicConfig(filename=filename, filemode='a', encoding='utf-8',
                        level=logging.DEBUG, style='{', format=FORMAT_MSG)
    
    return logging.getLogger()


if __name__ == '__main__':
    logger = get_logger()
    parse = argparse.ArgumentParser(description="Проводим операции с двумя матрицами")
    parse.add_argument('-m1', type=list, metavar='matrix1', nargs='+', default=[[8, 9, 7], [8, 5, 2], [7, 6, 7]],
                       help="1. Пример ввода значений (от 0 до 9): 012 345 678 910  |  [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 1, 0]]")
    parse.add_argument('-m2', type=list, metavar='matrix2', nargs='+', default=[[8, 9, 7], [8, 5, 2], [7, 6, 7]],
                       help="2. Пример ввода значений: abc 123 a1b +1/ | [['a', 'b', 'c'], [1, 2, 3], ['a', 1, 'b'], ['+', 1, '/']]")
    parse.add_argument('-o', metavar='operation', default='+',
                       help="сложения матриц: -o '+' | умножение матриц: -o '*' | сравнение матриц: -o '==' ")
    args = parse.parse_args()

    try:
        matrix1 = Matrix(args.m1)
        logger.info(f'Cоздан: matrix1 = {str(matrix1)}')
        matrix2 = Matrix(args.m2)
        logger.info(f'Cоздан: matrix2 = {str(matrix2)}')
        operation = args.o
        logger.info(f"Cоздан: operation = '{operation}'")

        print('\nРезультат формирования матриц:')
        print(f'matrix1: {matrix1}')
        print(f'matrix2: {matrix2}')

        if operation == '+':
            print('\nВывод результата сложения матриц:')
            result = f'matrix1 + matrix2 = {matrix1 + matrix2}'
            print(result)
            logger.info(result)
        elif operation == '*':
            print('\nВывод результата умножения матриц:')
            result = f'matrix1 * matrix2 = {matrix1 * matrix2}'
            print(result)
            logger.info(result)
        elif operation == '==':
            print('\nВывод результата сравнения матриц:')
            result = f'matrix1 == matrix2 | {matrix1 == matrix2}'
            print(result)
            logger.info(result)
        else:
            print(f"\nОперация '{operation}' не найдена.\nДоступные операции:\nСложения матриц: '+'\nУмножение матриц: '*'\nСравнение матриц: '=='")

        print('\nВывод документации:')
        print(Matrix.__doc__)
        print(Matrix.__init__.__doc__)
        print(Matrix.__add__.__doc__)
        print(Matrix.__mul__.__doc__)
        print(Matrix.__eq__.__doc__)
        print(Matrix.__str__.__doc__)
    except (ValFormatMatrixError) as err:
        print(err)
        logger.error(err)
