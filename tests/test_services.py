from src.services import get_top_transactions, get_cards_info

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