from src.utils import get_greeting

def main(date_time: str) -> dict:
    return {
        "greeting": get_greeting(date_time),
        "cards": get_cards_info(...),
        "top_transactions": get_top_transactions(...),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(),
    }