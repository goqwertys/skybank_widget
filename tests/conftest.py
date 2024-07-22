from tempfile import NamedTemporaryFile

import pytest
import pandas as pd


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    })
