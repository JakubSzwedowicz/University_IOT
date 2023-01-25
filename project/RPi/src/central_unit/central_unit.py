from typing import Dict
from paho.mqtt.client import MQTTMessage
from datetime import datetime

from common.communication import IPublisherSubscriber, MessageParser
from ...database.scripts.utils import DatabaseAdapter, DatabaseData
from ...src.utils.utils import get_ip_address, get_port, get_devices_configuration, ServerConfig
from .devices import AuthorizedDevices


class CentralUnit(IPublisherSubscriber):
    __DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS = 'device_mac_address'
    __DEVICES_CONFIGURATION_DOOR_DESCRIPTION = 'door_description'
    __DEVICES_CONFIGURATION_DOOR_ACCESS_LEVEL = 'door_access_level'
    __FUNCTIONS_HANLDER__MESSAGE_HANDLER = 'handler'
    __FUNCTIONS_HANDLER__PARSER = 'parser'
    __FUNCTIONS_HANDLER__REQEUST = 'request'
    __FUNCTIONS_HANDLERS__ACCEPTED = 'accepted'
    __FUNCTIONS_HANDLERS__DECLINED = 'declined'
    __TOPIC_DOOR_ACCESS = 'authorization/door_access'

    def __init__(self, ip_address: str = get_ip_address(), port: int = get_port()):
        super().__init__(ip_address, port, self.on_message)
        self.server_config = ServerConfig.get_config()
        # mac_address: AuthorizedDevices
        self._mac_address_authorized_device_mapping: Dict[str, AuthorizedDevices] = {
        }
        self.functions_handler = {}
        self._cards_statuses = {'active': 1,
                                'inactive': 2}
        self._authorization_message_status = {'request': 1,
                                              'accepted': 2,
                                              'declined': 3}
        self._build_devices_set()

    def run(self):
        try:
            self.connect()
            self._subscribe_and_handle_responses()
            while True:
                pass
        except KeyboardInterrupt as ex:
            print(f'Exception occurred: "{ex}"')
        finally:
            self.disconnect()

    def _subscribe_and_handle_responses(self) -> None:
        for topic in self.server_config.get_topics():
            super().subscribe(topic)
            self._add_response_handler(topic)

    def on_message(self, client, userdata, message):
        print(
            f'Received message from topic "{message.topic}" and payload "{message.payload.decode("utf-8")}"')
        if message.topic in self.functions_handler:
            self.functions_handler[message.topic][self.__FUNCTIONS_HANLDER__MESSAGE_HANDLER](
                message)

    def _build_devices_set(self):
        devices_mapping = get_devices_configuration()['devices']
        for device in devices_mapping.values():
            try:
                if self.__DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS not in device \
                        or self.__DEVICES_CONFIGURATION_DOOR_DESCRIPTION not in device \
                        or self.__DEVICES_CONFIGURATION_DOOR_ACCESS_LEVEL not in device:
                    print(f'Incomplete device configuration: "{device}"\n \
                        mac_address = "{self.__DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS not in device}"\
                        door_description = "{self.__DEVICES_CONFIGURATION_DOOR_DESCRIPTION not in device}"\
                        door_access_level = "{self.__DEVICES_CONFIGURATION_DOOR_ACCESS_LEVEL not in device}"')
                    continue
                # self._devices[device[self.__MAC_ADDRESS]] = AuthorizedDevices(device['door_access_level'], device['device_mac_address'], device['door_desciption'])
                query_result = DatabaseAdapter.Select.Where.get_device_door_access_level_by_mac_address(
                    device[self.__DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS])
                database_device, database_door, database_access_level = query_result

                if database_device is None:
                    query_result = DatabaseAdapter.Insert.add_device_door_access_level_to_database(
                        device[self.__DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS],
                        device[self.__DEVICES_CONFIGURATION_DOOR_DESCRIPTION],
                        device[self.__DEVICES_CONFIGURATION_DOOR_ACCESS_LEVEL])
                    database_device, database_door, database_access_level = query_result

                if database_device is None or database_door is None or database_access_level is None:
                    print(
                        f'Error while adding device with mac address "{device[self.__DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS]}" to database!')
                else:
                    self._mac_address_authorized_device_mapping[device[self.__DEVICES_CONFIGURATION_DEVICE_MAC_ADDRESS]] = AuthorizedDevices(
                        database_access_level.level, database_device._id, database_device.mac_address)
            except Exception as ex:
                print(f'Error while building devices set: "{ex}"')

    def _add_response_handler(self, topic: str) -> None:
        if topic == self.__TOPIC_DOOR_ACCESS:
            print(f'Adding response handler for "{topic}"')
            self.functions_handler[self.__TOPIC_DOOR_ACCESS] = self._get_handlers_for_door_access(
            )

    def _get_handlers_for_door_access(self) -> Dict[str, callable]:
        return {
            self.__FUNCTIONS_HANLDER__MESSAGE_HANDLER: self._handle_message_for_door_access_authorization,
            self.__FUNCTIONS_HANDLER__PARSER: MessageParser.DoorAccessMessage,
            self.__FUNCTIONS_HANDLER__REQEUST: self._handle_message_request_for_door_access_authorization
        }

    def _handle_message_for_door_access_authorization(self, message: MQTTMessage) -> None:
        handlers = self.functions_handler[self.__TOPIC_DOOR_ACCESS]
        parser = handlers[self.__FUNCTIONS_HANDLER__PARSER]

        messageStatus, device_mac_address, rfid_tag = parser.Request.deserialize(
            message)

        if messageStatus not in handlers:
            print(f'Unknown message status: "{messageStatus}"!')
            return
        if device_mac_address not in self._mac_address_authorized_device_mapping:
            print(f'Unknown device mac address: "{device_mac_address}"!')
            return

        query_result = DatabaseAdapter.Select.Where.get_card_status_card_employee_access_level_by_rfid_tag(
            rfid_tag)
        if (query_result is None):
            print(
                f'Error while getting card status, card, employee and access level by rfid tag: "{rfid_tag}"!')
            self.send(self.__TOPIC_DOOR_ACCESS, MessageParser.DoorAccessMessage.Response.serialize(
                self.__FUNCTIONS_HANDLERS__DECLINED, device_mac_address, rfid_tag))
            return
            
        database_card_status, database_card, database_employee, database_access_level = (query_result if query_result is not None else (
            None, DatabaseData.Definitions.Card(0, rfid_tag, 0, self._cards_statuses['inactive']), None, None))
        DatabaseAdapter.Insert.add_authorization_message_to_database(datetime.now(),
                                                                     database_card._id,
                                                                     self._mac_address_authorized_device_mapping[
                                                                         device_mac_address]._id,
                                                                     self._authorization_message_status[messageStatus])

        handlers[messageStatus](
            database_card_status, database_card, database_employee, database_access_level, self._mac_address_authorized_device_mapping[device_mac_address])

    def _handle_message_request_for_door_access_authorization(self, database_card_status: DatabaseData.Definitions.CardStatus,
                                                              database_card: DatabaseData.Definitions.Card,
                                                              database_employee: DatabaseData.Definitions.Employee,
                                                              database_access_level: DatabaseData.Definitions.AccessLevel,
                                                              authorized_device: AuthorizedDevices) -> None:
        date = None
        cardId = database_card._id
        deviceId = authorized_device._id
        authorization_message_status = None

        if (database_card_status is not None and database_card_status.status == 'active') \
                and (database_access_level is not None and int(database_access_level.level[1]) >= int(authorized_device.access_level[1])):
            authorization_message_status = self.__FUNCTIONS_HANDLERS__ACCEPTED
        else:
            authorization_message_status = self.__FUNCTIONS_HANDLERS__DECLINED

        self.send(self.__TOPIC_DOOR_ACCESS, MessageParser.DoorAccessMessage.Response.serialize(
            authorization_message_status, authorized_device.mac_address, database_card.rfid_tag))

        date = datetime.now()
        print(f'DATA: {date}')
        DatabaseAdapter.Insert.add_authorization_message_to_database(
            date, cardId, deviceId, self._authorization_message_status[authorization_message_status])
