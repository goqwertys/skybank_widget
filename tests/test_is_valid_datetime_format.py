import pytest

from src.utils import is_valid_datetime_format


@pytest.mark.parametrize(
    "string", [
        "2019-05-31 14:50:14",
        "2020-07-15 18:30:00",
        "1980-01-06 15:25:00"
        ]
)
def test_is_valid_datetime_format_true(string):
    assert is_valid_datetime_format(string)


@pytest.mark.parametrize(
    "string", [
        "",
        "1980-13-06 15:25:00",
        "hello world"
    ]
)
def test_is_valid_datetime_format_false(string):
    assert not is_valid_datetime_format(string)
