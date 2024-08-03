import json
import logging
import os.path
from typing import Literal

from src.config import (DATA_FOLDER, EVENTS_PAGE_INFO_FILENAME,
                        MAIN_PAGE_INFO_FILENAME, LOG_LEVEL)
from src.paths import get_project_root
from src.utils import is_valid_datetime_format
from src.views import get_events_page_info, get_main_page_info


# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = os.path.join(get_project_root(), 'logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

if __name__ == "__main__":
    """ Main logic """

    logger.info("Getting Started with the Program")
    while True:
        main_info_date = input("Введите дату в формате: YYYY-MM-DD HH:MM:SS для страницы 'Главная' или X для выхода\n")
        if main_info_date == "X" or is_valid_datetime_format(main_info_date):
            break
        print("Некорректный формат даты, введите дату в формате YYYY-MM-DD HH:MM:SS или X для выхода:")
    if main_info_date == "X":
        logger.warning("Home page data will not be retrieved")
        main_info_date = None
    logger.info(f"Data for the 'Main' page: {main_info_date}")

    while True:
        events_info_date = input("Введите дату в формате: YYYY-MM-DD HH:MM:SS для страницы 'События' или X для выхода\n")
        if events_info_date == "X" or is_valid_datetime_format(events_info_date):
            break
        print("Некорректный формат даты, введите дату в формате YYYY-MM-DD HH:MM:SS или X для выхода:")
    if events_info_date == "X":
        logger.warning("Event page data will not be retrieved")
        events_info_date = None

    while True:
        period = input(
            "Введите 'ALL', 'W', 'M', 'Y' для выбора периода для страницы 'События' или 'X' для пропуска\n")
        if period in ["ALL", "W", "M", "Y", "X"]:
            break
    if period == "X":
        logger.warning("Event page data will not be retrieved")
        events_info_date = None
    else:
        logger.info(f"Data for the 'Main' page: {main_info_date}")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if main_info_date:
        path = os.path.join(get_project_root(), DATA_FOLDER, MAIN_PAGE_INFO_FILENAME)
        main_info = get_main_page_info(main_info_date)
        with open(path, 'w') as f:
            json.dump(main_info, f, indent=4, ensure_ascii=False)
        logger.info(f"Data for the 'Main' page has been saved to {path}")
        print(f"Данные для страницы 'Главная' сохранены в {path}")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if events_info_date:
        path = os.path.join(get_project_root(), DATA_FOLDER, EVENTS_PAGE_INFO_FILENAME)
        events_info = get_events_page_info(events_info_date, "M")
        with open(path, 'w') as f:
            json.dump(events_info, f, indent=4, ensure_ascii=False)
        logger.info(f"Data for the 'Events' page has been saved to {path}")
        print(f"Данные для страницы 'Событрия' сохранены в {path}")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    logger.info("The program has completed its work")
