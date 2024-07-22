import os
import logging
import pandas as pd
from datetime import datetime

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


def start_of_month(dt: datetime) -> datetime:
    """Returns a datetime object representing the very beginning of the month in this datetime object"""
    return datetime(year=dt.year, month=dt.month, day=1, hour=0, minute=0, second=0, microsecond=0)
