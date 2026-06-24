from src.config import OPERATIONS_PATH
from src.config import SETTING_PATH
from src.services import get_cards_info
from src.services import get_currency_rates
from src.services import get_stock_prices
from src.services import get_top_transactions
from src.utils import filtered_operations_for_period
from src.utils import get_greeting
from src.utils import load_transactions
from src.utils import load_user_settings


def get_main_page(date_time: str | None = None) -> dict:
    settings = load_user_settings(SETTING_PATH)

    currencies = settings.get("user_currencies", [])

    operations = load_transactions(OPERATIONS_PATH)

    stocks = settings.get("user_stocks", [])

    filtered_operations = filtered_operations_for_period(operations, date_time)

    return {
        "greeting": get_greeting(date_time),
        "cards": get_cards_info(filtered_operations),
        "top_transactions": get_top_transactions(filtered_operations),
        "currency_rates": get_currency_rates(currencies),
        "stock_prices": get_stock_prices(stocks),
    }
