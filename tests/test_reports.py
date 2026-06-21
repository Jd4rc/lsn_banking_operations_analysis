import json
import pandas as pd

from src.reports import report_to_file

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