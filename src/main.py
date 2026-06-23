import json

from src.cashback import profitable_cashback_categories
from src.config import OPERATIONS_PATH
from src.reports import spending_by_category
from src.utils import load_transactions
from src.views import get_main_page

if __name__ == "__main__":
    operations = load_transactions(OPERATIONS_PATH)

    result = get_main_page()

    print("Главная страница")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    print("Выгодные категории кэшбека")
    print(profitable_cashback_categories(operations, 2026, 6))

    print("Траты по категории")
    print(spending_by_category(operations, "Супермаркеты"))
