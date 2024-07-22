"""Basic functions for generating JSON responses"""
from datetime import datetime

from src.config import GREETINGS_DICT
from src.config import NIGHT_MORNING
from src.config import MORNING_AFTERNOON
from src.config import AFTERNOON_EVENING
from src.config import EVENING_NIGHT


def greetings(datetime_str: str) -> str:
    """Returns greeting based on time"""
    night_morning = datetime.strptime(NIGHT_MORNING, '%H:%M:%S').time()
    morning_afternoon = datetime.strptime(MORNING_AFTERNOON, '%H:%M:%S').time()
    afternoon_evening = datetime.strptime(AFTERNOON_EVENING, '%H:%M:%S').time()
    evening_night = datetime.strptime(EVENING_NIGHT, '%H:%M:%S').time()

    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime_obj.time()

    if evening_night <= current_time < night_morning:
        greeting = GREETINGS_DICT.get("night")
    elif night_morning <= current_time < morning_afternoon:
        greeting = GREETINGS_DICT.get("morning")
    elif morning_afternoon <= current_time < afternoon_evening:
        greeting = GREETINGS_DICT.get("afternoon")
    else:
        greeting = GREETINGS_DICT.get("evening")

    return greeting
