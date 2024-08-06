import pytest

from src.views import greetings


@pytest.mark.parametrize('datetime_str, expected', [
    ("2024-07-22 09:30:00", "Доброе утро"),
    ("2024-07-22 15:30:00", "Добрый день"),
    ("2024-07-22 20:30:00", "Добрый вечер"),
    ("2024-07-22 02:30:00", "Доброй ночи")
])
def test_greetings(datetime_str, expected):
    assert greetings(datetime_str) == expected
