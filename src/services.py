import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv
from src.utils import load_user_settings

BASE_DIR = Path(__file__).resolve().parent.parent
SETTING_PATH = BASE_DIR / 'user_setting.json'

load_dotenv(BASE_DIR / '.env')

settings = load_user_settings(SETTING_PATH)

currencies = settings.get('user_currencies', [])
stocks = settings.get('user_stocks', [])


def get_cards_info(
        operations: list[dict],

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

def get_top_transactions(operations: list[dict]) -> list[dict]:
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

    api_key = os.getenv('API_KEY')

    currency_rates = []

    for currency in currencies:
        url = "https://api.apilayer.com/exchangerates_data/convert"

        params = {
            'from': currency,
            'to': 'RUB',
            'amount': 1
        }

        headers = {
            "apikey": api_key,
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

def get_stock_prices():
    ...