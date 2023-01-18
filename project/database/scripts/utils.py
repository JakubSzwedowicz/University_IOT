from configparser import ConfigParser
import psycopg2
from psycopg2.extras import execute_values
import json
from typing import List, Dict
from random import choice, randint
from faker import Faker

_faker = Faker()


def _read_json_file(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def config(filename=r"resources/config.ini", section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def is_database_empty() -> bool:
    optional_record = True
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute('SELECT * FROM access_level')

        optional_record = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return optional_record is None


class DatabaseData:
    _json_data_definitions = _read_json_file("resources/data_definitions.json")
    json_devices_configuration = _read_json_file("../RPi/devices_configuration.json")

    @staticmethod
    def get_database_entity_definition(entity: str) -> List[str]:
        json_dict = DatabaseData._json_data_definitions
        if entity not in json_dict:
            raise ValueError(
                f"Entity: {entity} not found in data_definitions.json")
        else:
            return json_dict[entity]

    @staticmethod
    def get_entities_from_devices_configuration(entity: str) -> Dict:
        json_dict = DatabaseData.json_devices_configuration
        if entity not in json_dict:
            raise ValueError(
                f"Entity: {entity} not found in data_definitions.json")
        else:
            return json_dict[entity]

    @staticmethod
    def get_access_level_entity_definition() -> List[str]:
        return DatabaseData.get_database_entity_definition("access_level")

    @staticmethod
    def get_card_status_entity_definition() -> List[str]:
        return DatabaseData.get_database_entity_definition("card_status")

    @staticmethod
    def get_authorization_message_status_entity_definition() -> List[str]:
        return DatabaseData.get_database_entity_definition("authorization_message_status")

    @staticmethod
    def get_device_entity_definitions() -> Dict:
        return DatabaseData.get_entities_from_devices_configuration("devices")
    

class Quries:
    @staticmethod
    def get_access_level_insert_query() -> str:
        return "INSERT INTO access_level (level) VALUES %s"

    @staticmethod
    def get_employee_insert_query() -> str:
        return "INSERT INTO employee (first_name, last_name, access_levelId) VALUES %s"

    @staticmethod
    def get_card_insert_query() -> str:
        return "INSERT INTO card (RFID_tag, employeeId, card_statusId) VALUES %s"

    @staticmethod
    def get_card_status_insert_query() -> str:
        return "INSERT INTO card_status (status) VALUES %s"

    @staticmethod
    def get_device_insert_query() -> str:
        return "INSERT INTO device (mac_address) VALUES %s"

    @staticmethod
    def get_door_insert_query() -> str:
        return "INSERT INTO door (description, deviceId, access_levelId) VALUES %s"

    @staticmethod
    def get_authorization_message_insert_query() -> str:
        return "INSERT INTO authorization_message (date, cardId, deviceId, authorization_message_statusId) VALUES %s"

    @staticmethod
    def get_authorization_message_status_insert_status() -> str:
        return "INSERT INTO authorization_message_status (status) VALUES %s"


class Generator:
    @staticmethod
    def gen_access_level(level: str) -> str:
        return f"'{level}',"

    @staticmethod
    def gen_card_status(status: str) -> str:
        return f"'{status}',"

    @staticmethod
    def gen_authorization_message_status(status: str) -> str:
        return f"'{status}',"

    @staticmethod
    def gen_employee(access_levels_ids_upper_bound: int) -> str:
        access_level_id = randint(1, access_levels_ids_upper_bound)
        return f"'{_faker.first_name()}', '{_faker.last_name()}', '{access_level_id}'"

    @staticmethod
    def gen_card(card_statuses_ids_upper_bound: int, employees_ids_upper_bound: int) -> str:
        rfid_tag = next(Generator._generator)
        employee_id = randint(1, employees_ids_upper_bound)
        card_status_id = randint(1, card_statuses_ids_upper_bound)
        return f"'{rfid_tag}', '{employee_id}', '{card_status_id}'"

    @staticmethod
    def gen_device(mac_accress: str) -> str:
        return f"'{mac_accress}',"

    @staticmethod
    def gen_door(description: str, device_id: int, access_level_id: int) -> str:
        return f"'{description}', '{device_id}', '{access_level_id}'"

    @staticmethod
    def gen_authorization_message(cards_ids_upper_bound: int, devices_ids_upper_bound: int, authorization_message_statuses_ids_upper_bound: int) -> str:
        card_id = randint(1, cards_ids_upper_bound)
        device_id = randint(1, devices_ids_upper_bound)
        authorization_message_status_id = randint(1, authorization_message_statuses_ids_upper_bound)
        return f"'{_faker.date_time()}', '{card_id}', '{device_id}', '{authorization_message_status_id}'"

    @staticmethod
    def _gen_unique_tag() -> int:
        tag = 123
        while True:
            yield tag
            tag += 1
    _generator = _gen_unique_tag()


def insert_many(insert_query, data):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        psycopg2.extras.execute_values(cur, insert_query, data)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
