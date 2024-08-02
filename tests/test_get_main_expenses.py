import pandas as pd
import pytest

from src.utils import get_main_expenses


def test_get_main_expenses_empty_df():
    df = pd.DataFrame()
    result_df = get_main_expenses(df)
    assert result_df.empty


def test_get_main_expenses_no_expenses():
    data = {
        'Категория': ['Еда', 'Транспорт'],
        'Сумма операции': [100.0, 50.0]
    }
    df = pd.DataFrame(data)
    result = get_main_expenses(df)
    assert result.empty


def test_get_main_expenses_with_expenses():
    data = {
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения', 'Транспорт', 'Еда', 'Развлечения', 'Жилье', 'Жилье', 'Здоровье'],
        'Сумма операции': [-100.0, -50.0, -75.0, -200.0, -30.0, -150.0, -100.0, -300.0, -250.0, -50.0]
    }
    # Жильё: 250 + 300 = 550
    # Развлечения 100 + 200 = 300
    # Еда 100 + 75 + 150 = 325
    # Транспорт 50 + 30 = 80
    # Здоровье 50
    # Остальное 0
    df = pd.DataFrame(data)
    result = get_main_expenses(df)
    expected = pd.DataFrame({
        'category': ['Жилье', 'Еда', 'Развлечения', 'Транспорт', 'Здоровье', 'Остальное'],
        'amount': [550.0, 325.0, 300.0, 80.0, 50.0, 0.0]
    })
    pd.testing.assert_frame_equal(result, expected)
