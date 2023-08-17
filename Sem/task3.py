# ✔ Доработаем задачу 2.
# ✔ Сохраняйте в лог файл раздельно:
# * уровень логирования,
# * дату события,
# * имя функции (не декоратора),
# * аргументы вызова,
# * результат.


import logging
from functools import wraps
from pathlib import Path


def get_logger():
    DIR_LOGS = Path.cwd() / 'logs'

    if not DIR_LOGS.is_dir():
        DIR_LOGS.mkdir()

    FORMAT_MSG = "{asctime} {levelname} {funcName}: {msg}"
    logging.basicConfig(filename='logs/tsk3.log', filemode='a', encoding='utf-8', level=logging.INFO, style='{',
    format=FORMAT_MSG)
    return logging.getLogger()


def log_decorator(func):
    @wraps(func)
    def wrapper(*args):
        logger = get_logger()
        try:
            result = func(*args)
        except:
            logger.error(f'ERORR! args={args}, {func.__name__}')
            return
        dict1 = {'funcname':func.__name__,'args': args, 'result': result}
        logger.info(dict1)
        return result

    return wrapper


@log_decorator
def sfunc(a, b):
    return a + b


if __name__ == '__main__':
    sfunc(5, 5)
    sfunc(10, -20)
    sfunc(0, 4, 15)
