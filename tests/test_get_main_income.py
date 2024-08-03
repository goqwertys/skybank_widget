import pandas as pd

from src.utils import get_main_income


def test_get_main_income_with_valid_data(main_income_df):
    expected_result = pd.DataFrame({
        "category": ["Зарплата", "Проценты", "Подарки"],
        "amount": [1500, 500, 100]
    }).sort_values(by="amount", ascending=False).reset_index(drop=True)

    result = get_main_income(main_income_df)
    pd.testing.assert_frame_equal(result, expected_result)


def test_get_main_income_with_empty_df():
    empty_df = pd.DataFrame(columns=["Категория", "Сумма операции"])
    expected_result = pd.DataFrame()

    result = get_main_income(empty_df)
    pd.testing.assert_frame_equal(result, expected_result)
