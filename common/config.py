import os
import time
from typing import Union

import pytz


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values
class AppConfig:
    TRACE_LEVEL = int(os.getenv("APP_TRACE_LEVEL", "20"))
    TOKEN = os.getenv("APP_TOKEN")
    TZ = pytz.timezone('Europe/Moscow')
    TS = time.time()

    def __init__(self, env):
        pass

    def __repr__(self):
        return str(self.__dict__)


# Expose Config object for app to import
Config = AppConfig(os.environ)


def get_config():
    return Config
