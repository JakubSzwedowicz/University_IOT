import json
from configparser import ConfigParser
from typing import Optional
from functools import lru_cache
from . import *

from common.utils import get_value_from_config

@lru_cache(maxsize=1)
def get_use_fake_central_unit() -> bool:
    filename = CONFIG_PATH
    section = CENTRAL_UNIT_SECTION
    option = CENTRAL_UNIT_RUN_CENTRAL_UNIT
    return get_value_from_config(filename, section, option, ConfigParser.getboolean)


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


def get_devices_configuration() -> Optional[dict]:
    filename = DEVICES_CONFIGURATION_PATH
    with open(filename, 'r') as file:
        return json.load(file)


class ServerConfig:
    def __init__(self, server_config: Optional[dict]):
        if ServerConfig._validate_json(server_config):
            self.name = server_config["config"]["name"]
            self.version = server_config["config"]["version"]
            self.description = server_config["config"]["description"]
            self.issuer = server_config["config"]["issuer"]
            self.topics = server_config['config']["topics"]
        else:
            print('Setting client config to default values')
            self.name = 'Default client config'
            self.version = '0.0.0'
            self.description = 'Using default configuration values'
            self.issuer = ''
            self.topics = {}

    def get_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return self.version

    def get_description(self) -> str:
        return self.description

    def get_issuer(self) -> str:
        return self.issuer

    def get_topics(self) -> dict:
        return self.topics

    @classmethod
    def get_config(cls, filename: str = f'{SERVER_CONFIG_PATH}') -> 'ServerConfig':
        try:
            with open(filename, 'r') as file:
                parsed_json = json.load(file)
                return ServerConfig(parsed_json)
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
            and "topics" in client_config["config"]


class _FuHandler:
    def __init__(self, handler: callable):
        self.handler = handler

    def handle(self, message: dict):
        self.handler(message)
        
class FunctionsHandler:
    def __init__(self, topic: str, message: dict):
        self.message = message
        self.topic = topic
        self._handlers = {}
    
    def on(self, trigger: object):
        if trigger in self._handlers:
            self._handlers[trigger].handle(self.message)
    
    def add_handler(self, handler: callable):
        pass