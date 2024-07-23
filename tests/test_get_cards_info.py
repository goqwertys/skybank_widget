import pandas as pd

from src.utils import get_cards_info


def test_get_cards_info_empty():
    df = pd.DataFrame()
    result = get_cards_info(df)
    assert result.empty


def test_get_cards_info(cards_data):
    expected_data = {
        "last_digits": ['1234', '5678'],
        "total_spent": [3000, 4000],
        "cashback": [30, 40]
    }
    expected_df = pd.DataFrame(expected_data)
    result = get_cards_info(cards_data)
    pd.testing.assert_frame_equal(result, expected_df)
