import json
from datetime import datetime
from pathlib import Path

import pandas as pd


def get_greeting() -> str:
    dt = datetime.now()
    hour = dt.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def load_user_settings(file_path: Path) -> dict:
    with open(file_path) as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError('Settings file must contain a JSON object')

    return data




def load_transactions(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден {file_path}")
    return pd.read_excel(file_path)


def filtered_operations_for_period(
    operations: pd.DataFrame,
) -> pd.DataFrame:
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    end_date = pd.to_datetime(date_time)
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)

    data = operations.copy()

    data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], errors="coerce", dayfirst=True)

    return data[(data["Дата платежа"] >= start_date) & (data["Дата платежа"] <= end_date)]
