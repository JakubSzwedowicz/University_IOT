import json
from configparser import ConfigParser
from typing import Optional
from functools import lru_cache
from . import *


def get_value_from_config(file_path: str, section: str, option: str, function: callable) -> Optional[bool or int or str]:
    parser = ConfigParser()
    value = None
    try:
        parser.read(file_path)
        if parser.has_section(section):
            value = function(parser, section=section, option=option)
    except Exception as ex:
        print(f'Error while reading config file: {ex}')
    finally:
        print(
            f'In file "{file_path}", section "{section}", option "{option}", , returning value of "{value}"')
        return value
