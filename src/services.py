import json
from pathlib import Path
import pandas as pd
import requests
from src.config import API_KEY


def get_cards_info(
        operations: pd.DataFrame,

) -> list[dict]:
    cards: dict[str, float] = {}

    for operation in operations:
        card_number = operation.get('Номер карты')
        amount = operation.get('Сумма платежа', 0)

        if not card_number:
            continue

        if amount >= 0:
            continue

        card_number = str(card_number)
        last_digits = card_number[-4:]

        cards[last_digits] = cards.get(last_digits, 0) + abs(amount)


    return [
        {
            'last_digits': last_digits,
            'total_spent': round(total_spent, 2),
            'cashback': round(total_spent/100, 2)
        }
        for last_digits, total_spent in cards.items()
    ]

def get_top_transactions(operations: pd.DataFrame) -> list[dict]:
    sorted_operations = sorted(
        operations,
        key=lambda operation: abs(operation['Сумма платежа']),
        reverse=True
    )

    top_operations = sorted_operations[:5]

    return [
        {
            "date": operation['Дата операции'],
            "amount": operation['Сумма платежа'],
            "category": operation['Категория'],
            "description": operation['Описание']
        }
        for operation in top_operations
    ]



def get_currency_rates(currencies: list[str]) -> list[dict]:
    # 3. для каждой валюты сделать запрос к API
    # 4. собрать список словарей
    # 5. вернуть результат


    currency_rates = []

    if API_KEY is None:
        raise ValueError(
            'API_KEY not found'
        )

    for currency in currencies:
        url = "https://api.apilayer.com/exchangerates_data/convert"

        params = {
            'from': currency,
            'to': 'RUB',
            'amount': 1
        }

        headers = {
            "apikey": API_KEY,
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout = 10)

            response.raise_for_status()

            data = response.json()
        except requests.RequestException:
            continue

        rate = data['result']

        if rate is None:
            continue


        currency_rates.append(
            {
                'currency': currency,
                'rate': round(rate, 2),
            }
        )

    return currency_rates

def get_stock_prices(
        stocks: list[str]
) -> list[dict]:
    result = []

    for stock in stocks:
        # Запрос к api
        ...

    result.append(
        {
            'stock': stock,
            'price': price
        }
    )

    return result