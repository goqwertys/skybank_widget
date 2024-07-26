import json
import os.path

from src.paths import get_project_root
from src.utils import fetch_intraday_data, get_closing_prices_for_symbol
from src.views import get_main_page_info


def main():
    path = os.path.join(get_project_root(), "data", "main_page.json")
    info = get_main_page_info("2019-05-31 14:50:14")
    with open(path, 'w') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)

    # data = fetch_intraday_data("AAPL", "2021-12-03 14:49:41") #03-12-2021 14:49:41
    # print(data)

    # symbols = ['AAPL', 'MSFT']
    # target_datetime = '2024-07-26 14:49:41'
    # closing_prices_df = get_closing_prices_for_symbol(symbols, target_datetime)
    # print(closing_prices_df)


if __name__ == "__main__":
    main()
