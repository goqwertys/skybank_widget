import os
import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
import logging

from src.external_api import get_currency_rates

load_dotenv()


@pytest.fixture
def mock_env_api_key(monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "test_api_key")


@pytest.fixture
def mock_requests_get():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": 70.0
    }
    with patch("requests.get", return_value=mock_response) as mock_get:
        yield mock_get


def test_get_currency_rates_success(mock_env_api_key, mock_requests_get):
    currencies = ["USD", "EUR"]
    expected_df = pd.DataFrame({
        "currency": ["USD", "EUR"],
        "rate": [70.0, 70.0]
    })

    result_df = get_currency_rates(currencies)
    pd.testing.assert_frame_equal(result_df, expected_df)


def test_get_currency_rates_exception():
    currencies = ["USD", "EUR"]
    expected_df = pd.DataFrame({
        "currency": ["USD", "EUR"],
        "rate": [0.0, 0.0]
    })

    with patch("requests.get", side_effect=requests.RequestException("Test exception")):
        result = get_currency_rates(currencies)
        pd.testing.assert_frame_equal(result, expected_df)


def test_get_currency_rates_empty_list(mock_env_api_key, mock_requests_get):
    currencies = []
    expected_df = pd.DataFrame(columns=["currency", "rate"])

    result_df = get_currency_rates(currencies)
    pd.testing.assert_frame_equal(result_df, expected_df)
