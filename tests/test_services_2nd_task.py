import json
import pandas as pd

from src.cashback import profitable_cashback_categories

def test_profitable_cashback_categories():
    data = pd.DataFrame(
        [
            {
                'Дата платежа': '2021-12-01',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -900
            },
            {
                'Дата платежа': '2021-12-16',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -800
            },
            {
                'Дата платежа': '2021-12-21',
                'Категория': 'Кафе',
                'Сумма платежа': -1000
            }
        ]
    )

    result = profitable_cashback_categories(data, 2021, 12)

    assert json.loads(result) == {
        'Супермаркеты': 17.0,
        'Кафе': 10.0
    }

def test_profitable_cashback_categories_other_month():
    data = pd.DataFrame(
       [ {
            'Дата платежа': '2021-08-01',
            'Категория': 'Супермаркеты',
            'Сумма платежа': -900
        }]
    )

    result = profitable_cashback_categories(data, 2021, 12)

    assert json.loads(result) == {}

def test_profitable_cashback_categories_skip_income():
    data = pd.DataFrame(
       [ {
            'Дата платежа': '2021-12-01',
            'Категория': 'Супермаркеты',
            'Сумма платежа': 900
        }]
    )

    result = profitable_cashback_categories(data, 2021, 12)

    assert json.loads(result) == {}

