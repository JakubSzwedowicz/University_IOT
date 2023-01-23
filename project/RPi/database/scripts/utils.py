import json
from random import randint
from typing import List, Dict, Tuple, Optional
from configparser import ConfigParser
from datetime import datetime

import psycopg2
from faker import Faker
from psycopg2.extras import execute_values

_faker = Faker()


def _read_json_file(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


class DatabaseData:
    _json_data_definitions = _read_json_file(
        "RPi/database/resources/data_definitions.json")
    json_devices_configuration = _read_json_file(
        "RPi/resources/devices_configuration.json")

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

    class Definitions:
        class Employee:
            def __init__(self, _id, first_name: str, last_name: str, access_level_id: int):
                self._id = id
                self.first_name = first_name
                self.last_name = last_name
                self._access_level_id = access_level_id

        class AccessLevel:
            def __init__(self, id: int, level: str):
                self._id = id
                self.level = level

        class Card:
            def __init__(self, id: int, rfid_tag: int, employee_id: int, card_status_id: int):
                self._id = id
                self.rfid_tag = rfid_tag
                self._employee_id = employee_id
                self._card_status_id = card_status_id

        class CardStatus:
            def __init__(self, id: int, status: str):
                self._id = id
                self.status = status
        
        class Device:
            def __init__(self, id: int, mac_address: str):
                self._id = id
                self.mac_address = mac_address
        
        class Door:
            def __init__(self, id: int, description: str, device_id: int, access_level_id: int):
                self._id = id
                self.description = description
                self._device_id = device_id
                self._access_level_id = access_level_id
        
        class AuthorizationMessage:
            def __init__(self, id: int, date: str, card_id: int, device_id: int, authorization_message_status_id: int):
                self._id = id
                self.date = date
                self._card_id = card_id
                self._device_id = device_id
                self._authorization_message_status_id = authorization_message_status_id
        
        class AuthorizationMessageStatus:
            def __init__(self, id: int, status: str):
                self._id = id
                self.status = status


class Quries:
    class Insert:
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
        def get_authorization_message_status_insert_query() -> str:
            return "INSERT INTO authorization_message_status (status) VALUES %s"

    class Select:
        @staticmethod
        def get_access_level_select_query() -> str:
            return "SELECT * FROM access_level"

        @staticmethod
        def get_employee_select_query() -> str:
            return "SELECT * FROM employee"

        @staticmethod
        def get_card_select_query() -> str:
            return "SELECT * FROM card"

        @staticmethod
        def get_card_status_select_query() -> str:
            return "SELECT * FROM card_status"

        @staticmethod
        def get_device_select_query() -> str:
            return "SELECT * FROM device"

        @staticmethod
        def get_door_select_query() -> str:
            return "SELECT * FROM door"

        @staticmethod
        def get_authorization_message_select_query() -> str:
            return "SELECT * FROM authorization_message"

        @staticmethod
        def get_authorization_message_status_select_query() -> str:
            return "SELECT * FROM authorization_message_status"

        class Where:
            @staticmethod
            def get_card_status_card_employee_access_level_by_rfid_tag_query() -> str:
                return "SELECT card_status.id, card_status.status, card.id, card.RFID_tag, card.employeeId, card.card_statusId, employee.id, employee.first_name, employee.last_name, employee.access_levelId, access_level.id, access_level.level FROM card \
                    INNER JOIN card_status ON card.card_statusId = card_status.id \
                    INNER JOIN employee ON card.employeeId = employee.id \
                    INNER JOIN access_level ON employee.access_levelId = access_level.id \
                    WHERE card.RFID_tag = {}"

            @staticmethod
            def get_device_door_access_level_by_mac_address_query() -> str:
                return "SELECT device.id, device.mac_address, door.id, door.description, door.deviceId, door.access_levelId, access_level.id, access_level.level FROM device \
                    INNER JOIN door ON device.id = door.deviceId \
                    INNER JOIN access_level ON door.access_levelId = access_level.id \
                    WHERE device.mac_address = '{}'"
            
            @staticmethod
            def get_employee_by_rfid_tag_query() -> str:
                return "SELECT * FROM employee \
                    WHERE id = \
                        (SELECT employeeId FROM card \
                            WHERE RFID_tag = '{}')"

            @staticmethod
            def get_access_level_card_by_rfid_tag_query() -> str:
                return "SELECT * FROM access_level \
                    Where id = \
                        (SELECT access_levelId FROM employee \
                            WHERE id = \
                                (SELECT employeeId FROM card \
                                    WHERE RFID_tag = {}) \
                        )"

            @staticmethod
            def get_card_status_by_rfid_tag_query() -> str:
                return "SELECT * FROM card_status \
                    WHERE id = \
                        (SELECT card_statusId FROM card \
                            WHERE RFID_tag = {})"
                            
                            
            @staticmethod
            def get_access_level_card_by_rfid_tag_query() -> str:
                return "SELECT * FROM access_level \
                    Where id = \
                        (SELECT access_levelId FROM employee \
                            WHERE id = \
                                (SELECT employeeId FROM card \
                                    WHERE RFID_tag = {}) \
                        )"

            @staticmethod
            def get_access_level_by_level_query() -> str:
                return "SELECT * FROM access_level WHERE level = '{}'"
            
            @staticmethod
            def get_door_by_deviceId_query() -> str:
                return "SELECT * FROM door WHERE deviceId = {}"
            
            @staticmethod
            def get_device_by_mac_address_query() -> str:
                return "SELECT * FROM device WHERE mac_address = '{}'"
            
            

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
        authorization_message_status_id = randint(
            1, authorization_message_statuses_ids_upper_bound)
        return f"'{_faker.date_time()}', '{card_id}', '{device_id}', '{authorization_message_status_id}'"

    @staticmethod
    def _gen_unique_tag() -> int:
        tag = 123
        while True:
            yield tag
            tag += 1
    _generator = _gen_unique_tag()


class DatabaseAdapter:
    @staticmethod
    def config(filename=r"RPi/database/resources/config.ini", section='postgresql') -> dict:
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

    @staticmethod
    def connect() -> None:
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = DatabaseAdapter.config()

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

    @staticmethod
    def is_database_empty() -> bool:
        optional_record = True
        conn = None
        try:
            params = DatabaseAdapter.config()
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

    @staticmethod
    def insert_many(insert_query, data) -> None:
        conn = None
        try:
            params = DatabaseAdapter.config()
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

    class Select:
        class Where:
            @staticmethod
            def get_card_status_card_employee_access_level_by_rfid_tag(rfid_tag: int) -> Tuple[DatabaseData.Definitions.CardStatus, DatabaseData.Definitions.Card, DatabaseData.Definitions.Employee, DatabaseData.Definitions.AccessLevel]:
                conn = None
                card_status = None
                card = None
                employee = None
                access_level = None
                try:
                    params = DatabaseAdapter.config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    filled_query = Quries.Select.Where.get_card_status_card_employee_access_level_by_rfid_tag_query().format(rfid_tag)
                    cur.execute(filled_query)

                    row = cur.fetchone()
                    expected_row_length = 11
                    if row is None or len(row) != expected_row_length:
                        raise Exception(
                            f'Wrong number of columns in query "{row}". Len: "{0 if row is None else len(row)}" instead of "{expected_row_length}"!')

                    card_status = DatabaseData.Definitions.CardStatus(
                        row[0], row[1])
                    card = DatabaseData.Definitions.Card(
                        row[2], row[3], row[4])
                    employee = DatabaseData.Definitions.Employee(
                        row[5], row[6], row[7], row[8])
                    access_level = DatabaseData.Definitions.AccessLevel(
                        row[9], row[10])

                    cur.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
                        return (card_status, card, employee, access_level) \
                            if (card_status is not None and card is not None and employee is None and access_level is None) \
                            else None
            
            @staticmethod
            def get_device_door_access_level_by_mac_address(mac_address: str) -> Tuple[DatabaseData.Definitions.Device, DatabaseData.Definitions.Door, DatabaseData.Definitions.AccessLevel]:
                conn = None
                device = None
                door = None
                access_level = None
                try:
                    params = DatabaseAdapter.config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    filled_query = Quries.Select.Where.get_device_door_access_level_by_mac_address_query().format(mac_address)
                    cur.execute(filled_query)

                    row = cur.fetchone()
                    expected_row_length = 8
                    if len(row) != expected_row_length:
                        raise Exception(
                            f'Wrong number of columns in query result "{row}": {len(row)}" instead of "{expected_row_length}"!')
                    
                    device = DatabaseData.Definitions.Device(row[0], row[1])
                    door = DatabaseData.Definitions.Door(row[2], row[3], row[4], row[5])
                    access_level = DatabaseData.Definitions.AccessLevel(row[6], row[7])
                    
                    cur.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
                        return (device, door, access_level) \
                            if device is not None and door is not None and access_level is not None \
                            else None
                            
            @staticmethod
            def get_device_by_mac_address(device_mac_address: str) -> Optional[DatabaseData.Definitions.Device]:
                conn = None
                device = None
                try:
                    params = DatabaseAdapter.config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    filled_query = Quries.Select.Where.get_device_by_mac_address_query().format(device_mac_address)
                    cur.execute(filled_query)

                    row = cur.fetchone()
                    expected_row_length = 2
                    if len(row) != expected_row_length:
                        raise Exception(
                            f'Wrong number of columns in query result, "{row}" instead of "{expected_row_length}"!')
                    
                    device = DatabaseData.Definitions.Device(row[0], row[1])
                    
                    cur.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
                    return device
                
            @staticmethod
            def get_access_level_by_level(level: str) -> Optional[DatabaseData.Definitions.AccessLevel]:
                conn = None
                access_level = None
                try:
                    params = DatabaseAdapter.config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    filled_query = Quries.Select.Where.get_access_level_by_level_query().format(level)
                    cur.execute(filled_query)

                    row = cur.fetchone()
                    expected_row_length = 2
                    if len(row) != expected_row_length:
                        raise Exception(
                            f'Wrong number of columns in query result, "{row}" instead of "{expected_row_length}"!')
                    
                    access_level = DatabaseData.Definitions.AccessLevel(row[0], row[1])
                    
                    cur.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
                    return access_level
                
            @staticmethod
            def get_door_by_deviceId(deviceId: int) -> Optional[DatabaseData.Definitions.Door]:
                conn = None
                door = None
                try:
                    params = DatabaseAdapter.config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    filled_query = Quries.Select.Where.get_door_by_deviceId_query().format(deviceId)
                    cur.execute(filled_query)

                    row = cur.fetchone()
                    expected_row_length = 4
                    if len(row) != expected_row_length:
                        raise Exception(
                            f'Wrong number of columns in query result, "{row}" instead of "{expected_row_length}"!')
                    
                    door = DatabaseData.Definitions.Door(row[0], row[1], row[2], row[3])
                    
                    cur.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
                    return door
    class Insert:
        @staticmethod
        def insert_device(mac_address: str) -> None:
            conn = None
            try:
                params = DatabaseAdapter.config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                filled_query = Quries.Insert.get_device_insert_query().format((mac_address,))
                cur.execute(filled_query)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    
        @staticmethod
        def insert_door(description: str, deviceId: int, access_levelId) -> None:
            conn = None
            try:
                params = DatabaseAdapter.config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                filled_query = Quries.Insert.get_door_insert_query().format((description, deviceId, access_levelId,))
                cur.execute(filled_query)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        
        @staticmethod            
        def add_device_door_access_level_to_database(device_mac_address: str, door_description: str, door_access_level: str) -> Tuple[DatabaseData.Definitions.Device, DatabaseData.Definitions.Door, DatabaseData.Definitions.AccessLevel]:
            device, door, access_level = DatabaseAdapter.Select.Where.get_device_door_access_level_by_mac_address(device_mac_address)
            if device is None:
                DatabaseAdapter.Insert.insert_device(device_mac_address)
                print('New device added into the database!')
                device = DatabaseAdapter.Select.Where.get_device_by_mac_address(device_mac_address)
            if access_level is None:
                access_level = DatabaseAdapter.Select.Where.get_access_level_by_level(door_access_level)
                if access_level is None:
                    raise Exception(
                        f'Could not find access level in database!')
            door = DatabaseAdapter.Select.Where.get_door_by_deviceId(device._id)
            if door is None:
                DatabaseAdapter.Insert.insert_door(door_description, device._id, access_level._id)
                print('New door added into the database!')
                door = DatabaseAdapter.Select.Where.get_door_by_deviceId(device._id)
            if door is None:
                print('Could not add door into the database!')
            return (device, door, access_level)
        
        @staticmethod
        def add_authorization_message_to_database(date: datetime, cardId: int, deviceId: int, authorization_message_statusId: int) -> None:
            conn = None
            try:
                params = DatabaseAdapter.config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                filled_query = Quries.Insert.get_authorization_message_insert_query().format((date, cardId, deviceId, authorization_message_statusId,))
                cur.execute(filled_query)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()