import logging
import os
from datetime import datetime

import pandas as pd

from src.config import LOG_LEVEL
from src.paths import get_project_root

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = os.path.join(get_project_root(), 'logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


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
    """Returns the top 5 transactions by amount"""
    logger.info("Calculating the top 5 transactions...")
    logger.debug(f"initial DataFrame:\n{df.head()}")

    if df.empty:
        logger.info("DataFrame is empty")
        return pd.DataFrame()

    top_5 = df.nlargest(5, 'Сумма операции')[['Дата операции', 'Сумма операции', 'Категория', 'Описание']]
    top_5 = top_5.rename(columns={
        'Дата операции': 'date',
        'Сумма операции': 'amount',
        'Категория': 'category',
        'Описание': 'description'
    })

    # Convert 'date' to string for consistent comparison
    top_5['date'] = top_5['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    logger.info(f"Resulting DataFrame:\n{top_5.head()}")

    return top_5
