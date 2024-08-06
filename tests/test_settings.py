import json
import logging
from unittest.mock import mock_open, patch

from src.utils import get_currencies, get_stocks

logger = logging.getLogger("utils")


@patch('src.utils.json.load')
@patch('builtins.open', new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_get_currencies_success(mock_file, mock_json_load):
    mock_json_load.return_value = {"user_currencies": ["USD", "EUR"]}
    result = get_currencies('settings.json')
    assert result == ["USD", "EUR"]
    mock_file.assert_called_with('settings.json', 'r')


@patch('builtins.open', new_callable=mock_open)
def test_get_currencies_file_not_found(mock_file):
    mock_file.side_effect = FileNotFoundError
    result = get_currencies("nonexistent.json")
    assert result == []


@patch('src.utils.json.load')
@patch('builtins.open', new_callable=mock_open, read_data='invalid json')
def test_get_currencies_json_decode_error(mock_file, mock_json_load):
    mock_json_load.side_effect = json.JSONDecodeError("Expecting value", 'invalid json', 0)
    result = get_currencies('invalid.json')
    assert result == []


@patch('builtins.open', new_callable=mock_open)
def test_get_currencies_other_exception(mock_file):
    mock_file.side_effect = Exception("Some unexpected error")
    result = get_currencies('settings.json')
    assert result == []


@patch('src.utils.json.load')
@patch('builtins.open',
       new_callable=mock_open,
       read_data='{"user_currencies": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}')
def test_get_stocks(mock_file, mock_json_load):
    mock_json_load.return_value = {"user_currencies": ["USD", "EUR"]}
    result = get_currencies('settings.json')
    assert result == ["USD", "EUR"]
    mock_file.assert_called_with('settings.json', 'r')


@patch('builtins.open', new_callable=mock_open)
def test_get_stocks_file_not_found(mock_file):
    mock_file.side_effect = FileNotFoundError
    result = get_currencies("nonexistent.json")
    assert result == []


@patch('src.utils.json.load')
@patch('builtins.open', new_callable=mock_open, read_data='invalid json')
def test_get_stocks_json_decode_error(mock_file, mock_json_load):
    mock_json_load.side_effect = json.JSONDecodeError("Expecting value", 'invalid json', 0)
    result = get_stocks('invalid.json')
    assert result == []


@patch('builtins.open', new_callable=mock_open)
def test_get_stocks_other_exception(mock_file):
    mock_file.side_effect = Exception("Some unexpected error")
    result = get_stocks('settings.json')
    assert result == []
