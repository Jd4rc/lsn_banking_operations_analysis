import pandas as pd
import requests

from src.cashback import logger
from src.config import ALPHA_VANTAGE_API_KEY
from src.config import EXCHANGE_RATES_API_KEY


def get_cards_info(
    operations: pd.DataFrame,
) -> list[dict]:
    """
    Формирует информацию по банковским картам.

    Для каждой карты рассчитывается общая сумма расходов
    и размер кешбэка. Учитываются только операции с
    отрицательной суммой платежа. Карты без номера
    пропускаются.

    :param operations: DataFrame с банковскими операциями.
    :return: Список словарей вида:
        [
            {
                "last_digits": "5814",
                "total_spent": 1262.0,
                "cashback": 12.62
            }
        ]
    """
    if "Номер карты" not in operations.columns:
        return []

    if "Сумма платежа" not in operations.columns:
        return []

    cards: dict[str, float] = {}

    for _, operation in operations.iterrows():
        card_number = operation["Номер карты"]
        amount = operation["Сумма платежа"]

        if pd.isna(card_number):
            continue

        if str(card_number).strip() == "":
            continue

        if amount >= 0:
            continue

        card_number = str(card_number)
        last_digits = card_number[-4:]

        cards[last_digits] = cards.get(last_digits, 0) + abs(amount)

    return [
        {
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": round(total_spent / 100, 2),
        }
        for last_digits, total_spent in cards.items()
    ]


def get_top_transactions(operations: pd.DataFrame) -> list[dict]:
    """
    Возвращает топ-5 транзакций по сумме платежа.

    Транзакции сортируются по модулю суммы платежа
    в порядке убывания. В результат включаются дата,
    сумма, категория и описание операции.

    :param operations: DataFrame с банковскими операциями.
    :return: Список словарей вида:
        [
            {
                "date": "2021-12-08",
                "amount": -564.0,
                "category": "Супермаркеты",
                "description": "Покупка в магазине"
            }
        ]
    """
    top_operations = (
        operations.assign(abs_amount=operations["Сумма платежа"].abs())
        .sort_values(by="abs_amount", ascending=False)
        .head(5)
    )

    return [
        {
            "date": pd.to_datetime(operation["Дата операции"]).strftime("%d-%m-%Y"),
            "amount": operation["Сумма платежа"],
            "category": operation["Категория"],
            "description": operation["Описание"],
        }
        for _, operation in top_operations.iterrows()
    ]


def get_currency_rates(currencies: list[str]) -> list[dict]:
    """
    Получает курсы валют по отношению к российскому рублю.

    Для каждой валюты выполняется запрос к API Exchange Rates Data.
    Если запрос завершается ошибкой или курс отсутствует,
    такая валюта пропускается.

    :param currencies: Список кодов валют (например, USD, EUR).
    :return: Список словарей вида:
        [
            {
                "currency": "USD",
                "rate": 78.45
            }
        ]
    :raises ValueError: Если не найден API-ключ.
    """
    currency_rates = []

    if EXCHANGE_RATES_API_KEY is None:
        raise ValueError("API_KEY not found")

    for currency in currencies:
        url = "https://api.apilayer.com/exchangerates_data/convert"

        params: dict[str, str | int | float]  = {"from": currency, "to": "RUB", "amount": 1}

        headers = {
            "apikey": EXCHANGE_RATES_API_KEY,
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            response.raise_for_status()

            data = response.json()
        except requests.RequestException as e:
            logger.warning("Ошибка при получении курса %s: %s", currency, e)
            continue

        rate = data["result"]

        if rate is None:
            continue

        currency_rates.append(
            {
                "currency": currency,
                "rate": round(rate, 2),
            }
        )

    return currency_rates


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """
    Получает текущую стоимость акций по указанным тикерам.

    Для каждого тикера выполняется запрос к API Alpha Vantage.
    В случае успешного ответа возвращается список словарей
    с названием акции и ее текущей стоимостью.

    :param stocks: Список тикеров акций.
    :return: Список словарей с информацией об акциях.
    """
    stock_prices = []

    for stock in stocks:
        # Запрос к api
        url = "https://www.alphavantage.co/query"

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": stock,
            "apikey": ALPHA_VANTAGE_API_KEY,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            continue

        quote = data.get("Global Quote", {})
        name = quote.get("01. symbol")
        price = quote.get("05. price")

        if price is None:
            continue

        stock_prices.append({"stock": name, "price": round(float(price), 2)})
    return stock_prices
