import os
import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

from src.external_api import get_stocks_prices

load_dotenv()


@pytest.fixture
def mock_env_api_key(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_api_key")


@pytest.fixture
def mock_requests_get():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Global Quote": {
            "05. price": "150.75"
        }
    }
    with patch("requests.get", return_value=mock_response) as mock_get:
        yield mock_get


def test_get_stocks_prices(mock_env_api_key, mock_requests_get):
    symbols = ["AAPL", "GOOGL"]
    expected_df = pd.DataFrame({
        "symbol": ["AAPL", "GOOGL"],
        "price": [150.75, 150.75]
    })

    result_df = get_stocks_prices(symbols)
    pd.testing.assert_frame_equal(result_df, expected_df)


def test_get_stocks_prices_exception(mock_env_api_key):
    symbols = ["AAPL", "GOOGL"]
    expected_df = pd.DataFrame({
        "symbol": ["AAPL", "GOOGL"],
        "price": [0.0, 0.0]
    })
    with patch("requests.get", side_effect=requests.RequestException("Test exception")):
        result_df = get_stocks_prices(symbols)
        pd.testing.assert_frame_equal(result_df, expected_df)


def test_get_stocks_prices_empty_list(mock_env_api_key, mock_requests_get):
    symbols = []
    expected_df = pd.DataFrame(columns=["symbol", "price"])

    result_df = get_stocks_prices(symbols)
    pd.testing.assert_frame_equal(result_df, expected_df)
