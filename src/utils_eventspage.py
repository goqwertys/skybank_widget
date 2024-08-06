import logging
import os
from datetime import datetime, timedelta
from typing import Literal

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
    logger.info(f"Time segment ({start_dt}, {end_dt})")
    return start_dt, end_dt


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


def get_total_expenses(df: pd.DataFrame) -> float:
    """ Returns the amount of expenses """
    logger.info("Getting total expenses...")
    logger.debug(f"Initial DataFrame:\n{df.shape}")

    if df.empty:
        logger.info("DataFrame is empty")
        return 0.0

    result = -df[df["Сумма платежа"] < 0]["Сумма платежа"].sum()
    logger.info(f"Total expenses: {result}")
    return round(result, 2)


def get_main_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """ Returns DataFrame of expenses by first most expensive categories the rest are combined into one """
    logger.info("Calculating the main expenses....")
    logger.debug(f"Initial DataFrame: {df.head()}")

    if df.empty:
        return pd.DataFrame()

    # Filtering expenses
    df_expenses = df[df["Сумма операции"] < 0].copy()  # Создаем копию среза
    if df_expenses.empty:
        return pd.DataFrame()

    df_expenses.loc[:, "Сумма операции"] = df_expenses["Сумма операции"].abs()

    # Grouping
    df_grouped = df_expenses.groupby("Категория")["Сумма операции"].sum().reset_index()

    # Sorting by values
    df_sorted = df_grouped.sort_values(by="Сумма операции", ascending=False)

    # Top 7
    top_categories = df_sorted.head(7).copy()  # Создаем копию

    # Combining the rest
    other_categories = df_sorted.iloc[7:]
    other_sum = other_categories["Сумма операции"].sum()
    other_row = pd.DataFrame({"category": ["Остальное"], "amount": [round(other_sum)]})

    # Renaming
    top_categories.rename(columns={'Категория': 'category', 'Сумма операции': 'amount'}, inplace=True)

    # Sorting result_df by amount in descending order
    top_categories = top_categories.sort_values(by='amount', ascending=False).reset_index(drop=True)

    # Union
    result_df = pd.concat([top_categories, other_row], ignore_index=True)

    logger.info(f"Final main expenses dataframe:\n{result_df.head()}")

    return result_df


def get_transfers_cash(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a DataFrame grouped by the categories "Наличные" and "Переводы"""
    logger.info("Calculating top 5 transactions...")
    logger.info(f"Initial dataframe:\n{df.head()}")
    # Filtering operations
    filtered_df = df[(df["Категория"].isin(["Наличные", "Переводы"])) & (df["Сумма операции"] < 0)]

    if filtered_df.empty:
        logger.info("No categories 'Переводы' 'Наличные'")
        result = pd.DataFrame({
            "category": ["Переводы", "Наличные"],
            "amount": [0.0, 0.0]
        }).sort_values(by="amount", ascending=False).reset_index(drop=True)
        logger.info(f"Final main expenses dataframe:\n{result}")
        return result
    else:
        grouped_df = filtered_df.groupby("Категория", as_index=False)["Сумма операции"].apply(lambda x: x.abs().sum())
        grouped_df.columns = ["category", "amount"]
        grouped_df.rename(columns={'Категория': 'category', 'Сумма операции': 'amount'}, inplace=True)
        result = grouped_df.sort_values(by="amount", ascending=False)
        result = result.reset_index(drop=True)
        logger.info(f"Final main expenses dataframe:\n{result.head()}")
        return result


def get_total_income(df: pd.DataFrame) -> float:
    """ Returns the amount of expenses """
    logger.info("Getting total expences...")
    logger.debug(f"Original DataFrame:\n{df.head()}")

    if df.empty:
        logger.info("DataFrame is empty")
        return 0.0

    result = df[df["Сумма платежа"] > 0]["Сумма платежа"].sum()
    logger.info(f"Total income = {result}")
    return result


def get_main_income(df: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame of income by first most expensive categories the rest are combined into one"""
    logger.info("Calculating the main income....")
    if df.empty:
        logger.info("Parameter df is empty, an empty Dataframe will be returned")
        return pd.DataFrame()

    df_income = df[df["Сумма операции"] > 0].copy()  # Создаем копию среза
    if df_income.empty:
        logger.info("No income found")
        return pd.DataFrame()

    # Grouping
    df_grouped = df_income.groupby("Категория")["Сумма операции"].sum().reset_index()

    # Sorting
    result = df_grouped.sort_values(by="Сумма операции", ascending=False)

    result.rename(columns={'Категория': 'category', 'Сумма операции': 'amount'}, inplace=True)
    result = result.reset_index(drop=True)
    logger.info(f"Final main income dataframe:\n{result.head()}")
    return result
