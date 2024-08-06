from io import BytesIO
from unittest.mock import patch

import pandas as pd

from src.utils import load_operations


def test_load_operations_success(sample_data):
    excel_buffer = BytesIO()
    sample_data.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    with patch("pandas.read_excel", return_value=sample_data) as mock_read_excel:
        df = load_operations("fake_path/operations.xlsx")
        mock_read_excel.assert_called_once_with("fake_path/operations.xlsx")
        pd.testing.assert_frame_equal(df, sample_data)


def test_load_operations_file_not_found():
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        df = load_operations("fake_path/operations.xlsx")
        assert df.empty


def test_load_operations_empty_data_error():
    with patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError):
        df = load_operations("fake_path/operations.xlsx")
        assert df.empty


def test_load_operations_unexpected_error():
    with patch("pandas.read_excel", side_effect=Exception("Unexpected Error")):
        df = load_operations("fake_path/operations.xlsx")
        assert df.empty
