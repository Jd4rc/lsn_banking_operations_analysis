from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import pandas as pd


def report_to_file(filename: str | None = None,):
    """
    Декоратор для записи результат отчетов в файл.

    Если имя файла не задано, создается файл с названиемм по умолчанию.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            output_filename = filename

            if output_filename is None:
                output_filename = f'{func.__name__}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

            output_path = Path(output_filename)

            if isinstance(result, pd.DataFrame):
                result.to_json(
                    output_path,
                    orient='records',
                    force_ascii=False,
                    indent=4
                )
            else:
                output_path.write_text(
                    str(result),
                    encoding='utf-8',
                )

            return result
        return wrapper
    return decorator

@report_to_file()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
):
    """""
    Возвращает траты по заданной категории за последниео три месяца.

    :param transactions: DataFrame с транзакциями
    :param category: Название категории.
    :param date: Дата отсчета. Если не передеана, используется текущая дата.
    :return: DataFrame с тратами по указанной категории.
    """""

    data = transactions.copy()

    if date is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date, errors='coerce')


    start_date = end_date - pd.DateOffset(months=3)

    data['Дата платежа'] = pd.to_datetime(
        data['Дата платежа'],
        errors='coerce',
    )

    result = data[
        (data['Дата платежа'] >= start_date)
        & (data['Дата платежа'] <= end_date)
        & (data['Категория'] == category)
        & (data['Сумма платежа'] < 0)
    ]

    return result