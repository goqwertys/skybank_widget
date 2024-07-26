import os

import pandas as pd
import pytest
import requests
from dotenv import load_dotenv

from src.utils import fetch_intraday_data, get_closing_price_at_time, get_closing_prices_for_symbol
from unittest.mock import patch, MagicMock


@patch('requests.get')
def test_fetch_intraday_data(mock_get, mock_data):
    symbol = 'AAPL'
    date = '2023-07-24'
    expected_df = pd.DataFrame(mock_data["results"])
    expected_df["t"] = pd.to_datetime(expected_df["t"], unit="ms")

    mock_get.return_value.json.return_value = mock_data
    mock_get.return_value.raise_for_status.return_value = None

    result_df = fetch_intraday_data(symbol, date)

    pd.testing.assert_frame_equal(result_df, expected_df)

    load_dotenv()
    api_key = os.getenv("POLYGON_IO_API_KEY")
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{date}/{date}"
    params = {
        "apiKey": api_key,
        "adjusted": "true"
    }
    mock_get.assert_called_once_with(url, params=params)


@patch('requests.get')
def test_fetch_intraday_data_http_error(mock_get):
    symbol = 'AAPL'
    date = '2023-07-24'

    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError

    result_df = fetch_intraday_data(symbol, date)

    assert result_df.empty


@patch('requests.get')
def test_fetch_intraday_data_no_results(mock_get):
    symbol = 'AAPL'
    date = '2023-07-24'

    mock_data = {}
    mock_get.return_value.json.return_value = mock_data
    mock_get.return_value.raise_for_status.return_value = None

    with pytest.raises(ValueError, match="No 'results' found in response data for AAPL on 2023-07-24"):
        fetch_intraday_data(symbol, date)


def test_get_closing_price_at_time():
    data = {
        't': [pd.to_datetime('2023-07-24 16:00:00'), pd.to_datetime('2023-07-24 17:00:00')],
        'c': [150.0, 152.0]
    }
    df = pd.DataFrame(data)
    target_time = "2023-07-24 16:00:00"
    closing_price = get_closing_price_at_time(df, target_time)
    assert closing_price == 150.0


@patch('src.utils.fetch_intraday_data')
@patch('src.utils.get_closing_price_at_time')
def test_get_closing_prices_for_symbol(mock_get_closing_price_at_time, mock_fetch_intraday_data):
    # Mock fetch_intraday_data and get_closing_price_at_time
    mock_fetch_intraday_data.return_value = pd.DataFrame({
        't': [pd.to_datetime('2021-10-01 09:30:00')],
        'c': [145.01]
    })
    mock_get_closing_price_at_time.return_value = 145.01

    # Call the function
    result = get_closing_prices_for_symbol(['AAPL', 'MSFT'], '2021-10-01 09:30:00')

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result['symbol'].tolist() == ['AAPL', 'MSFT']
    assert result['closing_price'].tolist() == [145.01, 145.01]
