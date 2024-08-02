import json
import os.path

import requests
from dotenv import load_dotenv

from src.external_api import get_stocks_prices
from src.paths import get_project_root
from src.utils import get_currencies, get_stocks
from src.views import get_main_page_info, get_events_page_info
from src.config import DATA_FOLDER, MAIN_PAGE_INFO_FILENAME
from src.config import USER_SETTINGS_FILENAME


if __name__ == "__main__":
    """ Main logic """
    ##############################
    path = os.path.join(get_project_root(), DATA_FOLDER, MAIN_PAGE_INFO_FILENAME)
    main_info = get_main_page_info("2019-05-31 14:50:14")
    with open(path, 'w') as f:
        json.dump(main_info, f, indent=4, ensure_ascii=False)
    ##############################
    events_info = get_events_page_info("2019-05-31 14:50:14", "")
    ##############################
    # path = os.path.join(get_project_root(), DATA_FOLDER, USER_SETTINGS_FILENAME)
    # symbols = get_stocks(path)
    #
    # print(symbols)
    # info = get_stocks_prices(symbols)
    # print(info)
    ##############################
    # symbol = "USD"
    # load_dotenv()
    # api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    # base_url = "https://www.alphavantage.co/query"
    # params = {
    #     "function": "GLOBAL_QUOTE",
    #     "symbol": symbol,
    #     "apikey": api_key
    # }
    # response = requests.get(base_url, params=params)
    # data = response.json()
    # print(data)
    ##############################
