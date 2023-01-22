from configparser import ConfigParser
from . import *
from typing import Optional
import json

def use_fake_device() -> bool:
    filename=CONFIG_PATH
    section=DEVICE_SECTION
    parser = ConfigParser()
    try: 
        parser.read(filename)
        if parser.has_section(section):
            return parser.getboolean(section=section, option=DEVICE_SECTION_RUN_FAKE_DEVICE)
    except Exception as ex:
        print(f'Error while reading config file: {ex}')
    finally:
        return True

def get_open_door_duration() -> Optional[int]:
    filename=CONFIG_PATH
    section=DEVICE_SECTION
    parser = ConfigParser()
    maybe_duration = None
    try: 
        parser.read(filename)
        if parser.has_section(section):
            maybe_duration = parser.getint(section=section, option=DEVICE_SECTION_OPEN_DOOR_DURATION)
    except Exception as ex:
        print(f'Error while reading config file: {ex}')
    finally:
        print(f'For section "{section}" in config file "{filename}, duration is "{maybe_duration}"')
        return maybe_duration 
    
def get_ip_address() -> Optional[str]:
    filename=CONFIG_PATH
    section=CONNECTION_SECTION
    parser = ConfigParser()
    try: 
        parser.read(filename)
        if parser.has_section(section):
            maybe_ip_address = parser.get(section=section, option=CONNECTION_SECTION_IP_ADDRESS)
            if not isinstance(maybe_ip_address, str):
                maybe_ip_address = None
        else:
            print(f'No section "{section}" in config file')
    except Exception as ex:
        print(f'Error while reading config file: {ex}')
    finally:
        print(f'For section "{section}" in config file "{filename}, IP address is "{maybe_ip_address}"')
        return maybe_ip_address

def get_port() -> Optional[int]:
    filename=CONFIG_PATH
    section=CONNECTION_SECTION
    parser = ConfigParser()
    maybe_port = None
    try: 
        parser.read(filename)
        if parser.has_section(section):
            maybe_port = parser.getint(section=section, option=CONNECTION_SECTION_PORT)
        else:
            print(f'File "{filename}" does not contain section "{section}"')
    except Exception as ex:
        print(f'Error while reading config file: {ex}')
    finally:
        print(f'For section "{section}" in config file "{filename}, port is "{maybe_port}" of type "{type(maybe_port)}"')
        return maybe_port
   
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
            print(f'Error while loading client configuration file: "{filename}" with error: "{ex}"')

    @staticmethod
    def _validate_json(client_config: dict) -> bool:
        return "config" in client_config \
                and "name" in client_config["config"] \
                and "version" in client_config["config"] \
                and "description" in client_config["config"] \
                and "issuer" in client_config["config"] \
                and "mac_address" in client_config["config"] \
                and "topics" in client_config["config"]