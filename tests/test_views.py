from src.views import main


def test_main():
    result = main("2026-06-16 10:00:00")

    assert result == {
        "greeting": "Доброе утро",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": [],
    }