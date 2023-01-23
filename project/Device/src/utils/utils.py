import json

from configparser import ConfigParser
from typing import Optional
from functools import lru_cache
from . import *

from common.utils import get_value_from_config

@lru_cache(maxsize=1)
def get_use_fake_device() -> bool:
    filename = CONFIG_PATH
    section = DEVICE_SECTION
    option = DEVICE_SECTION_RUN_FAKE_DEVICE
    return get_value_from_config(filename, section, option, ConfigParser.getboolean)


@lru_cache(maxsize=1)
def get_open_door_duration() -> Optional[int]:
    filename = CONFIG_PATH
    section = DEVICE_SECTION
    option = DEVICE_SECTION_OPEN_DOOR_DURATION
    return get_value_from_config(filename, section, option, ConfigParser.getfloat)


@lru_cache(maxsize=1)
def get_ip_address() -> Optional[str]:
    filename = CONFIG_PATH
    section = CONNECTION_SECTION
    option = CONNECTION_SECTION_IP_ADDRESS
    return get_value_from_config(filename, section, option, ConfigParser.get)


@lru_cache(maxsize=1)
def get_port() -> Optional[int]:
    filename = CONFIG_PATH
    section = CONNECTION_SECTION
    option = CONNECTION_SECTION_PORT
    return get_value_from_config(filename, section, option, ConfigParser.getint)


class ClientConfig:
    def __init__(self, client_config: Optional[dict]):
        if ClientConfig._validate_json(client_config):
            self.name = client_config["config"]["name"]
            self.version = client_config["config"]["version"]
            self.description = client_config["config"]["description"]
            self.issuer = client_config["config"]["issuer"]
            self.mac_address = client_config["config"]["mac_address"]
            self.topics = client_config['config']["topics"]
        else:
            print('Setting client config to default values')
            self.name = 'Default client config'
            self.version = '0.0.0'
            self.description = 'Using default configuration values'
            self.issuer = ''
            self.mac_address = ''
            self.topics = {}

    def get_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return self.version

    def get_description(self) -> str:
        return self.description

    def get_issuer(self) -> str:
        return self.issuer

    def get_mac_address(self) -> str:
        return self.mac_address

    def get_topics(self) -> dict:
        return self.topics

    @classmethod
    def get_config(cls, filename: str = f'{CLIENT_CONFIG_PATH}') -> 'ClientConfig':
        try:
            with open(filename, 'r') as file:
                parsed_json = json.load(file)
                return ClientConfig(parsed_json)
                None
        except Exception as ex:
            print(
                f'Error while loading client configuration file: "{filename}" with error: "{ex}"')

    @staticmethod
    def _validate_json(client_config: dict) -> bool:
        return "config" in client_config \
            and "name" in client_config["config"] \
            and "version" in client_config["config"] \
            and "description" in client_config["config"] \
            and "issuer" in client_config["config"] \
            and "mac_address" in client_config["config"] \
                and "topics" in client_config["config"]