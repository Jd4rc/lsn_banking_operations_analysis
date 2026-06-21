from unittest.mock import patch, Mock

import pytest
import requests

from src.services import get_top_transactions, get_cards_info, get_currency_rates

def test_get_top_transactions():
    operations = [
        {
            "Дата операции": "2026-06-16 10:00:00",
            "Сумма платежа": -100,
            "Категория": "Супермаркеты",
            "Описание": "Пятёрочка",
        },
        {
            "Дата операции": "2026-06-16 11:00:00",
            "Сумма платежа": -500,
            "Категория": "Переводы",
            "Описание": "Перевод",
        },
        {
            "Дата операции": "2026-06-16 12:00:00",
            "Сумма платежа": -50,
            "Категория": "Кафе",
            "Описание": "Кофе",
        },
    ]

    result = get_top_transactions(operations)

    assert result == [
        {
            "date": "2026-06-16 11:00:00",
            "amount": -500,
            "category": "Переводы",
            "description": "Перевод",
        },
        {
            "date": "2026-06-16 10:00:00",
            "amount": -100,
            "category": "Супермаркеты",
            "description": "Пятёрочка",
        },
        {
            "date": "2026-06-16 12:00:00",
            "amount": -50,
            "category": "Кафе",
            "description": "Кофе",
        },
    ]

def test_get_top_transactions_returns_only_five_items():
    operations = [
        {
            "Дата операции": f"2026-06-16 1{i}:00:00",
            "Сумма платежа": -i * 100,
            "Категория": "Категория",
            "Описание": f"Операция {i}",
        }
        for i in range(1, 8)
    ]

    result = get_top_transactions(operations)

    assert len(result) == 5
    assert result[0]["amount"] == -700
    assert result[-1]["amount"] == -300


def test_get_cards_info_single_card():
    operations = [
        {
            "Номер карты": "*4052",
            "Сумма платежа": -1000,
        },
        {
            "Номер карты": "*4052",
            "Сумма платежа": -500,
        },
    ]

    result = get_cards_info(operations)

    assert result == [
        {
            'last_digits': '4052',
            'total_spent': 1500,
            'cashback': 15.0
        }
    ]

def test_get_card_info(operations):
    result = get_cards_info(operations)

    assert result == [
        {
            "last_digits": "4052",
            "total_spent": 1500.0,
            "cashback": 15.0,
        },
        {
            "last_digits": "7813",
            "total_spent": 200.0,
            "cashback": 2.0,
        },
    ]

def test_get_cards_info_with_multiple_cards():
    operations = [
        {
            "Номер карты": "*5678",
            "Сумма платежа": -1500
        },
        {
            "Номер карты": "*9178",
            "Сумма платежа": -98
        }
    ]

    result = get_cards_info(operations)

    assert result == [
        {
            "last_digits": "5678",
            "total_spent": 1500.0,
            "cashback": 15.0,
        },
        {
            "last_digits": "9178",
            "total_spent": 98.0,
            "cashback": 0.98,
        }
    ]

def test_get_cards_info_with_sum_operations():
    operations = [
        {
            "Номер карты": "*5678",
            "Сумма платежа": -1000,
        },
        {
            "Номер карты": "*5678",
            "Сумма платежа": -500,
        },
    ]

    result = get_cards_info(operations)

    assert result == [
        {
            "last_digits": "5678",
            "total_spent": 1500.0,
            "cashback": 15.0,
        },
    ]


def test_get_cards_info_ignore_positive_amounts():
    operations = [
        {
            "Номер карты": "*5678",
            "Сумма платежа": 1000,
        },
        {
            "Номер карты": "*5678",
            "Сумма платежа": 500,
        },
    ]

    result = get_cards_info(operations)

    assert result == []

def test_get_cards_info_with_missing_card():
    operations = [
        {
            "Сумма платежа": -1000,
        },
        {
            "Сумма платежа": -500,
        },
    ]

    result = get_cards_info(operations)

    assert result == []


def test_get_cards_info_with_rounding():
    operations = [
        {
            "Номер карты": "*3456",
            "Сумма платежа": -1234.567,
        }
    ]

    result = get_cards_info(operations)


    assert result == [
        {
            "last_digits": "3456",
            "total_spent": 1234.57,
            "cashback": 12.35,
        },
    ]
@patch('src.services.EXCHANGE_RATES_API_KEY', 'test_api_key')
@patch('src.services.requests.get')
def test_get_currency_rates_success(mock_get):

    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        'result': 91.2345
    }
    mock_response.raise_for_status.return_value = None

    result = get_currency_rates(['USD'])

    assert result == [{'currency': 'USD', 'rate': 91.23}]

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        params={
            'from': 'USD',
            'to': 'RUB',
            'amount': 1,
        },
        headers={
            "apikey": 'test_api_key',
        },
        timeout=10
    )

@patch('src.services.EXCHANGE_RATES_API_KEY', 'test_api_key')
@patch('src.services.requests.get')
def test_get_currency_rates_multiple_currencies(mock_get):

    mock_response_usd = Mock()
    mock_response_usd.json.return_value = {
        'result': 91.2345
    }
    mock_response_usd.raise_for_status.return_value = None

    mock_response_eur = Mock()
    mock_response_eur.json.return_value = {
        'result': 87.8270
    }
    mock_response_eur.raise_for_status.return_value = None

    mock_get.side_effect = [
        mock_response_usd,
        mock_response_eur,
    ]

    result = get_currency_rates(['USD', 'EUR'])

    assert result == [
        {'currency': 'USD', 'rate': 91.23},
        {'currency': 'EUR', 'rate': 87.83},
    ]

@patch('src.services.EXCHANGE_RATES_API_KEY', 'test_api_key')
@patch('src.services.requests.get')
def test_get_currency_rates_skip_none_rate(mock_get):

    mock_response_usd = Mock()
    mock_response_usd.json.return_value = {
        'result': None
    }
    mock_response_usd.raise_for_status.return_value = None

    mock_get.side_effect = [
        mock_response_usd,
    ]

    result = get_currency_rates(['USD'])

    assert result == []


@patch('src.services.EXCHANGE_RATES_API_KEY', 'test_api_key')
@patch('src.services.requests.get', side_effect=requests.RequestException())
def test_get_currency_rates_skip_request_error(mock_get):
    result = get_currency_rates(['USD'])

    assert result == []


@patch('src.services.EXCHANGE_RATES_API_KEY', None)
def test_get_currency_rates_without_api_key():
    with pytest.raises(ValueError, match='API_KEY not found'):
        get_currency_rates(['USD'])






