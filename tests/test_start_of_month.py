from datetime import datetime
import pytest

from src.utils_mainpage import start_of_month


@pytest.mark.parametrize("input_datetime, expected", [
    (datetime(2024, 7, 22, 15, 30, 45), datetime(2024, 7, 1, 0, 0, 0)),
    (datetime(2024, 12, 15, 8, 10, 20), datetime(2024, 12, 1, 0, 0, 0)),
    (datetime(2024, 2, 1, 0, 0, 0), datetime(2024, 2, 1, 0, 0, 0)),
    (datetime(2024, 8, 31, 23, 59, 59), datetime(2024, 8, 1, 0, 0, 0)),
    (datetime(2024, 1, 1, 12, 00, 00), datetime(2024, 1, 1, 0, 0, 0))
])
def test_start_of_month(input_datetime, expected):
    assert start_of_month(input_datetime) == expected
