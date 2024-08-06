import pandas as pd

from src.utils_mainpage import get_top_5_transactions


def test_get_top_5_transactions_empty():
    df = pd.DataFrame()
    result = get_top_5_transactions(df)
    pd.testing.assert_frame_equal(df, result)


def test_get_top_5_transactions(transactions_data):
    expected_data = {
        'date': [
            '2024-07-28 19:20:21',
            '2024-07-30 20:21:22',
            '2024-07-25 17:18:19',
            '2024-07-15 09:10:11',
            '2024-07-10 13:14:15'
        ],
        'amount': [
            3500,
            3000,
            2500,
            2000,
            1800
        ],
        'category':
            ['Category I',
             'Category E',
             'Category D',
             'Category B',
             'Category G'
             ],
        'description': [
            'Description I',
            'Description E',
            'Description D',
            'Description B',
            'Description G'
        ]
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['date'] = pd.to_datetime(expected_df['date'], format='%Y-%m-%d %H:%M:%S')

    result = get_top_5_transactions(transactions_data)
    result['date'] = pd.to_datetime(result['date'], format='%Y-%m-%d %H:%M:%S')

    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True), check_like=True)
