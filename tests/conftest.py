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
