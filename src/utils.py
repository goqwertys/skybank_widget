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


def filter_by_current_month(df: pd.DataFrame, current_dt: datetime) -> pd.DataFrame:
    """Returns a filtered dataframe by time range and 'OK' status"""
    logger.info(f"Filtering dataframe by current month: {current_dt}")
    if df.empty:
        logger.info("Dataframe is empty")
        return df

    # Ensure the 'Дата операции' column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['Дата операции']):
        logger.info("Converting 'Дата операции' column to datetime format")
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    start_dt = start_of_month(current_dt)
    end_dt = current_dt

    logger.info(f"Filtering between {start_dt} and {end_dt}")

    # Filter by the date range and 'OK' status
    result = df[(df['Дата операции'].between(start_dt, end_dt)) & (df["Статус"] == "OK")]

    logger.info(f"Filtered dataframe size: {result.shape[0]}")

    return result


def get_cards_info(transactions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate data by unique card number to get total expenses and cashback"""
    logger.info("Starting data aggregation")

    if transactions.empty:
        logger.info("Dataframe is empty")
        return transactions

    logger.info("Grouping data by 'Номер карты'")
    aggregated_df: pd.DataFrame = transactions.groupby("Номер карты").agg(
        last_digits=('Номер карты', "first"),
        total_spent=('Сумма операции', 'sum'),
        cashback=('Сумма операции', lambda x: x.sum() // 100)
    ).reset_index(drop=True)

    logger.info("Aggregation complete")
    return aggregated_df


def get_top_5_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the top 5 transactions by amount with specific details"""
    logger.info("Starting to retrieve top 5 transactions")

    if df.empty:
        logger.info("Dataframe is empty")
        return df

    logger.info("Sorting dataframe by 'Сумма операции' in descending order")
    top_5_df = df.nlargest(5, 'Сумма операции')[['Дата операции', 'Сумма операции', 'Категория', 'Описание']]

    logger.info("Retrieved top 5 transactions")
    return top_5_df
