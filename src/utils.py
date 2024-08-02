from datetime import datetime, timedelta
import json
import os
from typing import Literal
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


# DATETIME
def start_of_month(dt: datetime) -> datetime:
    """Returns a datetime object representing the very beginning of the month in this datetime object"""
    return datetime(year=dt.year, month=dt.month, day=1, hour=0, minute=0, second=0, microsecond=0)


def get_time_segment(
        dt: datetime,
        period: Literal["ALL", "W", "M", "Y"]
) -> tuple[datetime, datetime]:
    def start_of_week(d: datetime) -> datetime:
        return d - timedelta(days=d.weekday())

    def end_of_week(d: datetime) -> datetime:
        return start_of_week(d) + timedelta(days=7)

    def start_of_month(d: datetime) -> datetime:
        return d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def end_of_month(d: datetime) -> datetime:
        next_month = d.replace(day=28) + timedelta(days=4)
        return next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def start_of_year(d: datetime) -> datetime:
        return d.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def end_of_year(d: datetime) -> datetime:
        return start_of_year(d).replace(year=d.year + 1)

    if period == "ALL":
        raise ValueError("Period 'ALL' is not supported for this function")
    elif period == "W":
        start_dt = start_of_week(dt).replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = end_of_week(dt).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "M":
        start_dt = start_of_month(dt)
        end_dt = end_of_month(dt)
    elif period == "Y":
        start_dt = start_of_year(dt)
        end_dt = end_of_year(dt).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError(f"Unknown period: {period}")

    return start_dt, end_dt


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


def filter_operations_by_period(
        df: pd.DataFrame,
        current_dt: datetime,
        period: Literal["ALL", "W", "M", "Y"]
) -> pd.DataFrame:
    """Returns a filtered dataframe by time range and 'OK' status"""
    logger.info(f"Filtering dataframe by {period}: {current_dt}")
    if df.empty:
        logger.info("Dataframe is empty")
        return df

    # Ensure the 'Дата операции' column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['Дата операции']):
        logger.info("Converting 'Дата операции' column to datetime format")
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    if period == "ALL":
        logger.info(f"Filtering all after current date {current_dt}")
        result = df[(df['Дата операции'] > current_dt) & (df['Статус'] == "OK")]
    else:
        start_dt, end_dt = get_time_segment(current_dt, period)
        logger.info(f"Filtering between {start_dt} and {end_dt}")
        result = df[(df['Дата операции'].between(start_dt, end_dt)) & (df['Статус'] == "OK")]

    return result


# DATA FRAMES
def get_cards_info(transactions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate data by unique card number to get total expenses and cashback"""
    logger.info("Starting data aggregation")

    if transactions.empty:
        logger.info("Dataframe is empty")
        return transactions

    logger.info("Grouping data by 'Номер карты'")
    aggregated_df: pd.DataFrame = transactions.groupby("Номер карты").agg(
        last_digits=('Номер карты', "first"),
        total_spent=('Сумма операции', lambda x: round(abs(x.sum()), 2)),
        cashback=('Сумма операции', lambda x: abs(x.sum()) // 100)
    ).reset_index(drop=True)

    logger.info("Aggregation complete")
    return aggregated_df


def get_top_5_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the top 5 transactions by amount"""
    logger.info("Start processing get_top_5_transactions()")
    logger.debug(f"Исходный DataFrame:\n{df}")

    if df.empty:
        logger.info("DataFrame is empty")
        return pd.DataFrame()

    top_5 = df.nlargest(5, 'Сумма операции')[['Дата операции', 'Сумма операции', 'Категория', 'Описание']]
    top_5.columns = ['date', 'amount', 'category', 'description']

    # Convert 'date' to string for consistent comparison
    top_5['date'] = top_5['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    logger.info("Finishing processing the get_top_5_transactions function")
    logger.info("Resulting DataFrame:\n{result_df}")

    return top_5


def get_total_expenses(df: pd.DataFrame) -> pd.DataFrame:
    pass


def get_main_expenses(df: pd.DataFrame) -> pd.DataFrame:
    pass


def get_transfers_cash(df: pd.DataFrame) -> pd.DataFrame:
    pass


def get_total_income(df: pd.DataFrame) -> pd.DataFrame:
    pass


def get_main_income(df: pd.DataFrame) -> pd.DataFrame:
    pass


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
