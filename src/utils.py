from datetime import datetime
import json
from pathlib import Path
import pandas as pd



def get_greeting(date_time: str) -> str:
    dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"

def load_user_settings(file_path:Path) -> dict:
    with open(file_path) as file:
        return json.load(file)


def load_transactions(file_path:Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f'Файл не найден {file_path}'
        )
    return pd.read_excel(file_path)
