def get_cards_info():
    ...

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