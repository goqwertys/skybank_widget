# -*- coding: utf-8 -*-
from datetime import datetime

import pandas as pd
import pytest

from src.utils import filter_operations_by_period


def test_filter_operations_by_period_all(test_df):
    current_dt = datetime(2023, 10, 14, 12, 30, 45)
    result = filter_operations_by_period(test_df, current_dt, "ALL")
    pd.testing.assert_frame_equal(result, test_df)


def test_filter_operations_by_period_week(df_week):
    current_dt = datetime(2024, 8, 7, 12, 30, 45)
    result = filter_operations_by_period(df_week, current_dt, "W")
    dt_start = datetime(2024, 8, 5, 0, 0, 0)
    dt_end = datetime(2024, 8, 12, 0, 0, 0)
    expected = df_week[(df_week['Дата операции'] >= dt_start) & (df_week['Дата операции'] < dt_end)]
    pd.testing.assert_frame_equal(result, expected)


def test_filter_operations_by_period_month(test_df):
    current_dt = datetime(2023, 10, 15, 12, 30, 45)
    result = filter_operations_by_period(test_df, current_dt, "M")
    expected = test_df.iloc[:2]
    pd.testing.assert_frame_equal(result, expected)


def test_filter_operations_by_period_year(test_df):
    current_dt = datetime(2023, 10, 15, 12, 30, 45)
    result = filter_operations_by_period(test_df, current_dt, "Y")
    expected = test_df.iloc[:3]
    pd.testing.assert_frame_equal(result, expected)


def test_filter_operations_by_period_empty_df():
    empty_df = pd.DataFrame(columns=['Дата операции', 'Статус'])
    current_dt = datetime(2023, 10, 15, 12, 30, 45)
    result = filter_operations_by_period(empty_df, current_dt, "ALL")
    pd.testing.assert_frame_equal(result, empty_df)


def test_filter_operations_by_period_non_datetime_column(df_week):
    non_datetime_df = df_week.copy()
    non_datetime_df['Дата операции'] = non_datetime_df['Дата операции'].astype(str)
    current_dt = datetime(2024, 8, 7, 12, 30, 45)
    result = filter_operations_by_period(non_datetime_df, current_dt, "W")

    # Преобразуем столбец 'Дата операции' в формат datetime для df_week
    df_week['Дата операции'] = pd.to_datetime(df_week['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    dt_start = datetime(2024, 8, 5, 0, 0, 0)
    dt_end = datetime(2024, 8, 12, 0, 0, 0)
    expected = df_week[(df_week['Дата операции'] >= dt_start) & (df_week['Дата операции'] < dt_end)]

    pd.testing.assert_frame_equal(result, expected)


def test_filter_operations_by_period_unknown_period(test_df):
    current_dt = datetime(2023, 10, 15, 12, 30, 45)
    with pytest.raises(ValueError):
        filter_operations_by_period(test_df, current_dt, "unknown")


def test_filter_operations_by_period_status_filter():
    data_with_status = {
        'Дата операции': ['15.10.2023 12:30:45', '16.10.2023 12:30:45', '01.11.2023 12:30:45', '01.01.2024 12:30:45'],
        'Статус': ['OK', 'Failed', 'OK', 'OK']
    }
    df_with_status = pd.DataFrame(data_with_status)
    current_dt = datetime(2023, 10, 15, 12, 30, 45)
    result = filter_operations_by_period(df_with_status, current_dt, "W")
    expected = df_with_status.iloc[:1]
    pd.testing.assert_frame_equal(result, expected)
