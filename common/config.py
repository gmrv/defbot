import ast
import os
import time
from typing import Union

import pytz

from common import utils


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values
class AppConfig:
    TZ = pytz.timezone('Europe/Moscow')
    TS = time.time()

    TRACE_LEVEL = int(os.getenv("APP_TRACE_LEVEL", "20"))
    TOKEN = os.getenv("APP_TOKEN")
    MASTER_ID = os.getenv("MASTER_ID")
    STOP_WORDS_FILE = os.getenv("STOP_WORDS_FILE", "words.txt")
    STOP_WORDS = []
    IS_ANTISPAM_ACTIVE = True

    TRUSTED_ID = []
    TRUSTED_USERNAME = []

    def __init__(self, env):
        self.update()

    def __repr__(self):
        return str(self.__dict__)

    def update(self):
        self.STOP_WORDS = utils.read_list_from_file(self.STOP_WORDS_FILE)
        self.load_trusted()

    def load_trusted(self):
        with open('trusted.txt', 'r') as file:
            for line in file:
                # Преобразование строки в словарь с использованием ast.literal_eval
                data_dict = ast.literal_eval(line.strip())

                # Проверка наличия 'id' и 'username' в словаре
                if 'id' in data_dict[0] and data_dict[0]['id'] is not None:
                    self.TRUSTED_ID.append(data_dict[0]['id'])

                if 'username' in data_dict[0]:
                    self.TRUSTED_USERNAME.append(data_dict[0]['username'])

# Expose Config object for app to import
Config = AppConfig(os.environ)


def get_config():
    return Config
