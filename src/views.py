"""Basic functions for generating JSON responses"""
import os.path
from datetime import datetime
from typing import Union, Dict, List

import pandas as pd

from src.config import GREETINGS_DICT
from src.config import NIGHT_MORNING
from src.config import MORNING_AFTERNOON
from src.config import AFTERNOON_EVENING
from src.config import EVENING_NIGHT
from src.paths import get_project_root
from src.utils import load_operations, filter_by_current_month, get_cards_info, get_top_5_transactions, get_currencies, \
    get_stocks, get_closing_prices_for_symbol


def greetings(datetime_str: str) -> str:
    """Returns greeting based on time"""
    night_morning = datetime.strptime(NIGHT_MORNING, '%H:%M:%S').time()
    morning_afternoon = datetime.strptime(MORNING_AFTERNOON, '%H:%M:%S').time()
    afternoon_evening = datetime.strptime(AFTERNOON_EVENING, '%H:%M:%S').time()
    evening_night = datetime.strptime(EVENING_NIGHT, '%H:%M:%S').time()

    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime_obj.time()

    if evening_night <= current_time < night_morning:
        greeting = GREETINGS_DICT.get("night")
    elif night_morning <= current_time < morning_afternoon:
        greeting = GREETINGS_DICT.get("morning")
    elif morning_afternoon <= current_time < afternoon_evening:
        greeting = GREETINGS_DICT.get("afternoon")
    else:
        greeting = GREETINGS_DICT.get("evening")

    return greeting


JSONType = Union[Dict[str, 'JSONType'], List['JSONType'], str, int, float, bool, None]


def get_main_page_info(datetime_str: str) -> JSONType:
    # loading and filtering operations
    load_path = os.path.join(get_project_root(), "data", "operations.xlsx")
    operations_df = load_operations(load_path)
    filtered_operations = filter_by_current_month(operations_df, pd.to_datetime(datetime_str))

    # Loading currencies and stocks from user_settings.json
    settings_path = os.path.join(get_project_root(), "data", "user_settings.json")
    currencies = get_currencies(settings_path)
    stocks = get_stocks(settings_path)

    # adding operations info
    result = {
        "greetings": greetings(datetime_str),
        "cards": get_cards_info(filtered_operations).to_dict(orient="records"),
        "top_transactions": get_top_5_transactions(filtered_operations).to_dict(orient="records"),
        "currency_rates": None,  # TODO
        "stock_prices": get_closing_prices_for_symbol(stocks, datetime_str).to_dict(orient="records")
    }

    return result
