import pytest

from src.utils import get_greeting


@pytest.mark.parametrize(
    "date_time, expected",
    [
        ("2026-06-16 06:00:00", "Доброе утро"),
        ("2026-06-16 11:59:59", "Доброе утро"),
        ("2026-06-16 12:00:00", "Добрый день"),
        ("2026-06-16 17:59:59", "Добрый день"),
        ("2026-06-16 18:00:00", "Добрый вечер"),
        ("2026-06-16 22:59:59", "Добрый вечер"),
        ("2026-06-16 23:00:00", "Доброй ночи"),
        ("2026-06-16 04:59:59", "Доброй ночи"),
    ],
)
def test_get_greeting(date_time, expected):
    assert get_greeting(date_time) == expected

def test_get_greeting_invalid_date():
    with pytest.raises(ValueError):
        get_greeting("16.06.2026")