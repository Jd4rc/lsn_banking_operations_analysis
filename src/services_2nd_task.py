import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)

def profitable_cashback_categories(
       data: pd.DataFrame,
        year: int,
        month:int,
) -> str:
    """
    Анализирует выгодность категорий повышенного кэшбека

    Учитываются расходы за указанный месяц и год
    По кажой категории считается сумма возможного кэшбека


    :param data: DataFrame с транзакциями
    :param year: Год анализа
    :param month: Месяц анализа
    :return: JSON - строка с суммой кэшбека по категориям.
    """

    logger.info('Started cashback categories analysis')

    transactions = data.copy()

    transactions['Дата платежа'] = pd.to_datetime(
        transactions['Дата платежа'],
        dayfirst=True,
        errors='coerce',
    )

    filtered_transactions = transactions[
        (transactions['Дата платежа'].dt.year == year)
        & (transactions['Дата платежа'].dt.month == month)
        & (transactions['Сумма платежа'] < 0)
    ]

    categories = (
        filtered_transactions
        .groupby('Категория')['Сумма платежа']
        .sum()
        .abs()
        .apply(lambda amount: round(amount * 0.01, 2))
        .to_dict()
    )

    logger.info('Finished cashback categories analysis')

    return json.dumps(
        categories,
        indent=4,
        ensure_ascii=False,
    )

