from src.utils import get_greeting

def main(date_time: str) -> dict:
    return {
        "greeting": get_greeting(date_time),
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": [],
    }