import paths
import os
import logging
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


def get_transactions(path: str) -> list[dict]:
    """Takes as input a path to XLSX file and returns a list of dictionaries with data about
        financial transactions."""
    try:
        data = pd.read_excel(path)
        result = data.to_dict(orient='records')
        logger.info(f"Operations have been successfully loaded from {path}")
        return [dict(item) for item in result]
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"No data found in file: {path}")
        return []
    except Exception as ex:
        logger.error(f"An error has occurred: {ex}")
        return []
