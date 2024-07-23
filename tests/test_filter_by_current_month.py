from datetime import datetime
import pandas as pd

from src.utils import filter_by_current_month


def test_filter_by_current_month(sample_df, expected_filtered):
    """Test the filter_by_current_month function"""
    current_dt = datetime(2024, 7, 31, 23, 59, 59)
    expected_filtered['Дата операции'] = pd.to_datetime(expected_filtered['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    result_df = filter_by_current_month(sample_df, current_dt)

    result_df = result_df.reset_index(drop=True)
    expected_df = expected_filtered.reset_index(drop=True)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_filter_by_current_month_empty_df():
    """Test filter_by_current_month with an empty DataFrame"""
    empty_df = pd.DataFrame(columns=['Дата операции', 'Статус'])
    current_dt = datetime(2024, 7, 31, 23, 59, 59)

    filtered_df = filter_by_current_month(empty_df, current_dt)

    assert filtered_df.empty


def test_filter_by_current_month_no_ok_status(sample_df):
    """Test filter_by_current_month with no 'OK' status"""
    sample_df['Статус'] = ['Failed', 'Failed', 'Failed', 'Failed']
    current_dt = datetime(2024, 7, 31, 23, 59, 59)

    filtered_df = filter_by_current_month(sample_df, current_dt)

    expected_data = {
        'Дата операции': [
            '01.07.2024 10:00:00',
            '15.07.2024 12:00:00',
            '25.07.2024 14:00:00'
        ],
        'Статус': ['Failed', 'Failed', 'Failed']
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['Дата операции'] = pd.to_datetime(expected_df['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    assert filtered_df.empty


def test_filter_by_current_month_outside_range(sample_df):
    """Test filter_by_current_month with dates outside the current month"""
    current_dt = datetime(2024, 8, 31, 23, 59, 59)

    filtered_df = filter_by_current_month(sample_df, current_dt)

    assert filtered_df.empty
