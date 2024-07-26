from datetime import datetime
import json
import os
import requests
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




logger = logging.getLogger(__name__)


def fetch_intraday_data(symbol: str, date: str) -> pd.DataFrame:
    """
        Fetch intraday data for a given symbol and date from Polygon.io.

        :param symbol: Stock symbol (e.g., 'AAPL')
        :param date: Date in the format 'YYYY-MM-DD'
        :return: DataFrame containing intraday data
    """
    logger.info(f"Requesting intraday data for {symbol} on {date}")
    load_dotenv()
    api_key = os.getenv("POLYGON_IO_API_KEY")

    # https://api.polygon.io/v2/aggs/ticker/AAPL/range/5/minute/2023-01-09/2023-02-10?adjusted=true&sort=asc&apiKey=eMo25X120lRfIAOZM7QpePv0biBFf1pu
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/{date}/{date}"
    params = {
        "apiKey": api_key,
        "adjusted": "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        data = response.json()

        if 'results' not in data:
            raise ValueError(f"No 'results' found in response data for {symbol} on {date}")

        df = pd.DataFrame(data['results'])
        df['t'] = pd.to_datetime(df['t'], unit='ms')
        logger.info(f"Data fetched successfully for {symbol} on {date}")
        return df
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data for {symbol} on {date}. An error occurred: {e}")
        return pd.DataFrame()


def get_closing_price_at_time(df: pd.DataFrame, target_daytime: str) -> float:
    """
        Get the closing price at a specific datetime from the DataFrame.

        :param df: DataFrame containing intraday data
        :param target_daytime: Target datetime in the format 'YYYY-MM-DD HH:MM:SS'
        :return: Closing price at the specified datetime
    """
    target_dt = pd.to_datetime(target_daytime)
    closest_dt = df['t'].sub(target_dt).abs().idxmin()
    closing_price = df.iloc[closest_dt]['c']
    logger.info(f"Closing price for target datetime {target_daytime}: {closing_price}")
    return closing_price


def get_closing_prices_for_symbol(symbols: list[str], target_datetime: str) -> pd.DataFrame:
    """
        Get closing prices for a list of stock symbols on a specific date at a specific time.

        :param symbols: List of stock symbols (e.g., ['AAPL', 'MSFT'])
        :param target_datetime: Date in the format 'YYYY-MM-DD HH:MM:SS'
        :return: DataFrame containing closing prices for each symbol
    """
    prices = []

    for symbol in symbols:
        intraday_data = fetch_intraday_data(symbol, target_datetime.split()[0])
        if not intraday_data.empty:
            closing_price = get_closing_price_at_time(intraday_data, target_datetime)
            if closing_price is not None:
                prices.append({
                    "symbol": symbol,
                    "closing_price": closing_price
                })

    prices_df = pd.DataFrame(prices)
    logger.info(f"DataFrame with closing prices: {prices_df}")
    return prices_df
