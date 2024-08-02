import requests
import os
import pandas as pd
import logging
from dotenv import load_dotenv

from src.config import LOG_LEVEL
from src.paths import get_project_root

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = os.path.join(get_project_root(), 'logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_currency_rates(currencies: list[str]) -> pd.DataFrame:
    """ Returns a dataframe of currency rates"""

    load_dotenv()
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    headers = {"apikey": api_key}
    result = []

    if not currencies:
        return pd.DataFrame(columns=["currency", "rate"])

    for currency in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            rate = data["result"]
        except requests.RequestException as e:
            logger.info(f"Error fetching exchange rate data for {currency}: {e}")
            rate = 0.0
        result.append({
            "currency": currency,
            "rate": rate
        })

    return pd.DataFrame(result)


def get_stocks_prices(symbols: list[str]) -> pd.DataFrame:
    """ Returns a dataframe of stocks rates"""
    load_dotenv()
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    base_url = "https://www.alphavantage.co/query"
    result = []

    for symbol in symbols:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            quote = data["Global Quote"]
            result.append({
                "symbol": symbol,
                "price": float(quote["05. price"]),
            })
        except requests.RequestException as e:
            logger.info(f"Error fetching stock quote data for {symbol}: {e}")
            result.append({
                "symbol": symbol,
                "price": 0.0,
            })

    return pd.DataFrame(result)
