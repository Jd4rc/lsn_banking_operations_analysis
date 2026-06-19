import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / 'data'

SETTING_PATH = DATA_DIR / 'user_settings.json'

OPERATIONS_PATH = DATA_DIR / 'user_operations.xlsx'

load_dotenv(BASE_DIR / '.env')

API_KEY = os.getenv('API_KEY')


