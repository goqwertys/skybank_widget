from datetime import datetime
import pytest

from src.utils import get_time_segment


def test_get_time_segment_week():
    dt = datetime(2023, 10, 15, 12, 30, 45)  # Воскресенье
    start_dt, end_dt = get_time_segment(dt, "W")
    assert start_dt == datetime(2023, 10, 9, 0, 0, 0)  # Понедельник
    assert end_dt == datetime(2023, 10, 16, 0, 0, 0)  # Следующий понедельник


def test_get_time_segment_month():
    dt = datetime(2023, 10, 15, 12, 30, 45)
    start_dt, end_dt = get_time_segment(dt, "M")
    assert start_dt == datetime(2023, 10, 1, 0, 0, 0)
    assert end_dt == datetime(2023, 11, 1, 0, 0, 0)


def test_get_time_segment_year():
    dt = datetime(2023, 10, 15, 12, 30, 45)
    start_dt, end_dt = get_time_segment(dt, "Y")
    assert start_dt == datetime(2023, 1, 1, 0, 0, 0)
    assert end_dt == datetime(2024, 1, 1, 0, 0, 0)


def test_get_time_segment_unknown_period():
    dt = datetime(2023, 10, 15, 12, 30, 45)
    with pytest.raises(ValueError):
        get_time_segment(dt, "unknown")


def test_get_time_segment_end_of_year():
    dt = datetime(2023, 12, 31, 23, 59, 59)
    start_dt, end_dt = get_time_segment(dt, "M")
    assert start_dt == datetime(2023, 12, 1, 0, 0, 0)
    assert end_dt == datetime(2024, 1, 1, 0, 0, 0)


def test_get_time_segment_start_of_week():
    dt = datetime(2023, 10, 16, 12, 30, 45)  # Понедельник
    start_dt, end_dt = get_time_segment(dt, "W")
    assert start_dt == datetime(2023, 10, 16, 0, 0, 0)
    assert end_dt == datetime(2023, 10, 23, 0, 0, 0)


def test_get_time_segment_end_of_week():
    dt = datetime(2023, 10, 22, 12, 30, 45)  # Воскресенье
    start_dt, end_dt = get_time_segment(dt, "W")
    assert start_dt == datetime(2023, 10, 16, 0, 0, 0)
    assert end_dt == datetime(2023, 10, 23, 0, 0, 0)


def test_get_time_segment_start_of_month():
    dt = datetime(2023, 10, 1, 0, 0, 0)
    start_dt, end_dt = get_time_segment(dt, "M")
    assert start_dt == datetime(2023, 10, 1, 0, 0, 0)
    assert end_dt == datetime(2023, 11, 1, 0, 0, 0)


def test_get_time_segment_end_of_month():
    dt = datetime(2023, 10, 31, 23, 59, 59)
    start_dt, end_dt = get_time_segment(dt, "M")
    assert start_dt == datetime(2023, 10, 1, 0, 0, 0)
    assert end_dt == datetime(2023, 11, 1, 0, 0, 0)


def test_get_time_segment_start_of_year():
    dt = datetime(2023, 1, 1, 0, 0, 0)
    start_dt, end_dt = get_time_segment(dt, "Y")
    assert start_dt == datetime(2023, 1, 1, 0, 0, 0)
    assert end_dt == datetime(2024, 1, 1, 0, 0, 0)
