import json
import pandas as pd
import os

from src.reports import report_to_file
from src.reports import spending_by_category


def test_report_to_file_with_dataframe(tmp_path):
    file_path = tmp_path / 'report.json'

    @report_to_file(str(file_path))
    def test_func():
        return pd.DataFrame(
            [
                {'Категория': 'Супермаркеты', 'Сумма платежа': -1000},
                {'Категория': 'Транспорт', 'Сумма платежа': -500},
            ]
        )

    result = test_func()

    assert file_path.exists()
    assert isinstance(result, pd.DataFrame)

    with open(file_path, encoding='UTF-8') as f:
        data = json.load(f)


    assert data == [
        {'Категория': 'Супермаркеты', 'Сумма платежа': -1000},
        {'Категория': 'Транспорт', 'Сумма платежа': -500},
    ]


def test_report_to_file_with_text_result(tmp_path):
    file_path = tmp_path / 'report.txt'

    @report_to_file(str(file_path))
    def test_func():
        return 'Hello report'


    result = test_func()
    assert file_path.exists()
    assert result == 'Hello report'
    assert file_path.read_text(encoding='UTF-8') == 'Hello report'

def test_report_to_file_default_filename(tmp_path):
    old_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        @report_to_file()
        def test_func():
            return 'default filename result'

        result = test_func()

        files = list(tmp_path.glob('test_func_*.json'))

        assert result == 'default filename result'
        assert len(files) == 1
        assert files[0].read_text(encoding='UTF-8') == 'default filename result'

    finally:
        os.chdir(old_cwd)


def test_spending_by_category_return_only_selected_category():
    transactions = pd.DataFrame(
        [
            {
                'Дата платежа': '2021-05-15',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -800
            },
            {
                'Дата платежа': '2021-05-15',
                'Категория': 'Кафе',
                'Сумма платежа': -1500
            }
        ]
    )

    result = spending_by_category(
        transactions,
        category='Кафе',
        date='2021-07-08',
    )

    assert len(result) == 1
    assert result.iloc[0]['Категория'] == 'Кафе'

def test_spending_by_category_return_only_last_three_months():
    transactions = pd.DataFrame(
        [
            {
                'Дата платежа': '2021-01-15',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -800
            },
            {
                'Дата платежа': '2021-03-15',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -1500
            },
            {
                'Дата платежа': '2021-07-15',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -1500
            },
            {
                'Дата платежа': '2021-09-15',
                'Категория': 'Супермаркеты',
                'Сумма платежа': -1500
            },

        ]
    )

    result = spending_by_category(
        transactions,
        category='Супермаркеты',
        date='2021-09-16',
    )

    assert len(result) == 2
    assert result['Сумма платежа'].to_list() == [-1500, -1500]