from src.config import SETTING_PATH
from src.config import OPERATIONS_PATH
from src.utils import get_greeting
from src.services import get_cards_info
from src.services import get_top_transactions
from src.services import get_currency_rates
from src.services import get_stock_prices
from src.utils import load_user_settings
from src.utils import load_transactions

def get_main_page() -> dict:
    settings = load_user_settings(SETTING_PATH)

    currencies = settings.get('user_currencies', [])

    operations = load_transactions(OPERATIONS_PATH)

    stocks = settings.get('user_stocks', [])

    return {
        "greeting": get_greeting(),
        "cards": get_cards_info(operations),
        "top_transactions": get_top_transactions(operations),
        "currency_rates": get_currency_rates(currencies),
        "stock_prices": get_stock_prices(stocks),
    }