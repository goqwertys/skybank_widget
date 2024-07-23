from tempfile import NamedTemporaryFile

import pytest
import pandas as pd


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    })


@pytest.fixture
def sample_df():
    """Fixture to create a sample DataFrame for testing (current date is 31.07.2024 10:00:00)"""
    data = {
        'Дата операции': [
            '25.06.2024 10:00:00',
            '15.07.2024 12:00:00',
            '25.07.2024 14:00:00',
            '01.07.2024 16:00:00',
        ],
        'Статус': ['OK', 'Failed', 'OK', 'OK']
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def expected_filtered():
    """Fixture to create an expected filtered DataFrame for testing (current date is 31.07.2024 10:00:00)"""
    expected_data = {
        'Дата операции': [
            '25.07.2024 14:00:00',
            '01.07.2024 16:00:00',
        ],
        'Статус': ['OK', 'OK']
    }
    expected_df = pd.DataFrame(expected_data)
    return expected_df


@pytest.fixture
def cards_data():
    data = {
        'Дата операции': [
            '2024-07-01 12:34:56',
            '2024-07-15 09:10:11',
            '2024-07-20 14:15:16',
            '2024-07-25 17:18:19'
        ],
        'Номер карты': ['1234', '1234', '5678', '5678'],
        'Сумма операции': [1000, 2000, 1500, 2500],
        'Кешбэк': [10, 20, 15, 25],
        'Статус': ['OK', 'OK', 'OK', 'OK']
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%Y-%m-%d %H:%M:%S")
    return df


@pytest.fixture
def transactions_data():
    data = {
        'Дата операции': [
            '2024-07-01 12:34:56',
            '2024-07-15 09:10:11',
            '2024-07-20 14:15:16',
            '2024-07-25 17:18:19',
            '2024-07-30 20:21:22',
            '2024-07-05 10:11:12',
            '2024-07-10 13:14:15',
            '2024-07-18 16:17:18',
            '2024-07-28 19:20:21',
            '2024-07-22 08:09:10'
        ],
        'Сумма операции': [
            1000,
            2000,
            1500,
            2500,
            3000,
            800,
            1800,
            500,
            3500,
            1200
        ],
        'Категория': [
            'Category A',
            'Category B',
            'Category C',
            'Category D',
            'Category E',
            'Category F',
            'Category G',
            'Category H',
            'Category I',
            'Category J'
        ],
        'Описание': [
            'Description A',
            'Description B',
            'Description C',
            'Description D',
            'Description E',
            'Description F',
            'Description G',
            'Description H',
            'Description I',
            'Description J'
        ]
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%Y-%m-%d %H:%M:%S")
    return df

