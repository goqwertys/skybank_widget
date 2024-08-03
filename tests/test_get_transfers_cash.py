import pandas as pd
import pytest
from unittest.mock import patch

from src.utils import get_transfers_cash


def test_get_transfers_cash_with_valid_data(transfers_cash_data):
    expected_result = pd.DataFrame({
        "category": ["Переводы", "Наличные"],
        "amount": [700, 500]
    }).sort_values(by="amount", ascending=False).reset_index(drop=True)

    result = get_transfers_cash(transfers_cash_data)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result)


def test_get_transfers_cash_with_empty_df():
    empty_df = pd.DataFrame(columns=["Категория", "Сумма операции"])
    expected_result = pd.DataFrame({
        "category": ["Переводы", "Наличные"],
        "amount": [0.0, 0.0]
    }).sort_values(by="amount", ascending=False).reset_index(drop=True)

    result = get_transfers_cash(empty_df)
    pd.testing.assert_frame_equal(result, expected_result)
