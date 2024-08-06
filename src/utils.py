import json
import logging
import os
from datetime import datetime

import pandas as pd

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


# DATA
def load_operations(path: str) -> pd.DataFrame:
    """Takes as input a path to XLSX file and returns a list of dictionaries with data about
        financial transactions."""
    try:
        data = pd.read_excel(path)
        logger.info(f"Operations have been successfully loaded from {path}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        logger.error(f"No data found in file: {path}")
        return pd.DataFrame()
    except Exception as ex:
        logger.error(f"An error has occurred: {ex}")
        return pd.DataFrame()


# SETTINGS
def get_currencies(settings: str) -> list[str]:
    """ Returns list of currencies from settings file"""
    try:
        with open(settings, 'r') as f:
            data = json.load(f)
            currencies = [currency for currency in data["user_currencies"]]
            logger.info(f"Retrieved currencies: {currencies}")
            return currencies
    except FileNotFoundError:
        logger.error(f"File not found: {settings}")
        return []
    except json.JSONDecodeError:
        logger.error(f"JSON decode error in file: {settings}")
        return []
    except Exception as ex:
        logger.error(f"An error has occurred: {ex}")
        return []


def get_stocks(settings: str) -> list[str]:
    """ Returns list of stocks from settings file"""
    try:
        with open(settings, 'r') as f:
            data = json.load(f)
            stocks = [price for price in data["user_stocks"]]
            logger.info(f"Retrieved stocks: {stocks}")
            return stocks
    except FileNotFoundError:
        logger.error(f"File not found: {settings}")
        return []
    except json.JSONDecodeError:
        logger.error(f"JSON decode error in file: {settings}")
        return []
    except Exception as ex:
        logger.error(f"An error has occurred: {ex}")
        return []


def is_valid_datetime_format(date_string):
    """ Checks if a string is valid for conversion to datetime """
    try:
        datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
