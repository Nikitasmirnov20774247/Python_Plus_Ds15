# ✔ Функция получает на вход текст вида: “1-й четверг ноября”,
# “3-я среда мая” и т.п.
# ✔ Преобразуйте его в дату в текущем году.
# ✔ Логируйте ошибки, если текст не соответсвует формату.


import logging
from functools import wraps
from pathlib import Path
import datetime


def get_logger():
    DIR_LOGS = Path.cwd() / 'logs'

    if not DIR_LOGS.is_dir():
        DIR_LOGS.mkdir()

    FORMAT_MSG = "{asctime} {levelname} {funcName}: {msg}"
    logging.basicConfig(filename='logs/tsk4.log', filemode='a', encoding='utf-8',
                        level=logging.INFO, style='{', format=FORMAT_MSG)
    
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
        dict1 = {'funcname': func.__name__, 'args': args, 'result': result}
        logger.info(dict1)
        return result

    return wrapper


@log_decorator
def func_date(a):
    logger = get_logger()
    month_list = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
                'августа', 'сентября', 'октября', 'ноября', 'декабря']
    week_day_list = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    date_list = a.split()
    try:
        date_list[0] = int(date_list[0].split('-')[0])
    except:
        logger.error(f'ERORR! date_list[0]={date_list[0]}, {func_date.__name__}')
        return
    try:
        date_list[1] = week_day_list.index(date_list[1])
    except:
        logger.error(f'ERORR! date_list[1]={date_list[1]}, {func_date.__name__}')
        return
    try:
        date_list[2] = month_list.index(date_list[2])
    except:
        logger.error(f'ERORR! date_list[2]={date_list[2]}, {func_date.__name__}')
        return
    year = datetime.datetime.now().year
    count = 0
    for day in range(1, 31):
        date_current = datetime.datetime(year=year, month=date_list[2], day=day)
        if date_current.weekday() == date_list[1]:
            count += 1
            if count == date_list[0]:
                return date_current
    logger.error(f'ERORR! no date {a}, {func_date.__name__}')



if __name__ == '__main__':
    print(func_date('1-й четверг ноября'))
    print(func_date('2-ая среда августа'))
    print(func_date('10-ая среда августа'))
    print(func_date('2-ая среда авгус'))
    print(func_date('втор-ая среда августа'))
    print(func_date('2-ая сред августа'))
