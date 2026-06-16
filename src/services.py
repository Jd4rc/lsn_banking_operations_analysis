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



def get_currency_rates():
    ...

def get_stock_prices():
    ...