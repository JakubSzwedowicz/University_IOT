from time import sleep, time
import json
from paho.mqtt.client import MQTTMessage
from typing import Optional, List

from src.peripherials.buzzer_handler import BuzzerHandler
from src.peripherials.card_reader_handler import RFIDHandler
from src.peripherials.leds_handler import LEDHandler
from src.utils.communication import *
from src.utils.utils import get_ip_address, get_port, get_open_door_duration, ClientConfig
from src.utils.utils import CLIENT_CONFIG_PATH


class _Callback:
    def __init__(self, callback: callable, duration: 0.5, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.time_start = time()
        self.time_duration = duration
        self._is_done = False

    def is_done(self) -> bool:
        return self._is_done

    def reset(self) -> None:
        self.time_start = time()
        self._is_done = False

    def __call__(self, *args, **kwargs) -> None:
        if time() - self.time_start > self.time_duration:
            self.callback(*args, **kwargs)
            self._is_done = True


class DeviceHandler(IPublisherSubscriber):
    __RESPONSE_CALL_NOW = 'now'
    __RESPONSE_CALL_CALLBACKS = 'callbacks'
    __RESPONSE_CALL_HANDLER = 'handler'
    __RESPONSE_CALL_PARSER = 'parser'
    __RESPONSE_CALL_ACCEPTED = 'accepted'
    __RESPONSE_CALL_DECLINED = 'declined'
    __TOPIC_DOOR_ACCESS = 'authorization/door_access'

    def __init__(self, ip_address: str = get_ip_address(), port: int = get_port(), door_open_duration: int = get_open_door_duration()):
        print(f'DeviceHandler: ip_address: {ip_address}, port: {port}, door_open_duration: {door_open_duration}')
        super().__init__(ip_address, port, self.process_message)
        self.client_config = ClientConfig.get_config()
        self.device_reaction_duration = door_open_duration
        self.RFID_handler = RFIDHandler()
        self.buzzer = BuzzerHandler()
        self.led = LEDHandler()
        self.authorization_message_statuses = [
            "request", "accepted", "declined"]
        self.message_response_handlers = {}
        self.sent_messages: set = set()
        self.current_callback: Optional[List[_Callback]] = None
        self._runnable = self._run

        self._subscribe_and_handle_responses()

    def run(self):
        print(f'IP address: {self.ip_address}')
        
        self._runnable()

    def _run(self):
        self.connect()
        while True:
            self.main_loop()
        self.disconnect()
    
    def _change_runnable(self, new_runnable: callable):
        self._runnable = new_runnable
        
    def main_loop(self):
        sleep(0.1)
        print('Checking for RFID Card...')
        maybe_uid = self.RFID_handler.read()
        if maybe_uid is not None:
            print(f'RFID Card Detected "{maybe_uid}"')
            self.send_door_access_request(maybe_uid)
        else:
            print("No RFID Card Detected")
        self.process_callables()
        
    def process_callables(self) -> None:
        to_remove = []
        print('Inside process_callables')
        if self.current_callback is not None:
            print('Processing callables...')
            for call in self.current_callback:
                if not call.is_done():
                    print('Calling...')
                    call()
                else:
                    print('About to remove...')
                    to_remove.append(call)
            if self.to_remove is not None:
                for removable in to_remove:
                    print('Removing...')
                    self.current_callback.remove(removable)

    def process_message(self, client, userdata, message: MQTTMessage) -> None:
        message_handler = self.message_response_handlers[message.topic][self.__RESPONSE_CALL_HANDLER]
        message_handler(message)

    def _handle_message_for_door_access_authorization(self, message: MQTTMessage):
        handlers = self.message_response_handlers[self.__TOPIC_DOOR_ACCESS]
        parser = handlers[self.__RESPONSE_CALL_PARSER]

        messageStatus, device_mac_address, rfid_tag = parser.Response.deserialize(
            message)

        if self.client_config.get_mac_address() == device_mac_address:
            if rfid_tag not in self.sent_messages:
                print(f'Received response with wrong rfid tag: "{rfid_tag}"!')
            if messageStatus not in handlers:
                print(f'Unknown message status: "{messageStatus}"!')
                return

            message_handlers = handlers[messageStatus]
            for call in message_handlers[self.__RESPONSE_CALL_NOW]:
                call()

            self.current_callback = [
                _Callback(*args) for args in message_handlers[self.__RESPONSE_CALL_CALLBACKS]]

    def _request_accepted(self):
        self.buzzer.on()
        self.led.set_green()
        print('Door is open')

    def _request_declined(self):
        self.buzzer.on()
        self.led.set_red()
        print('Door is closed')

    def _accepted_callback(self):
        self.led.clear()
        print('Door is closed')

    def _declined_callback(self):
        self.led.clear()
        print('Door is closed')

    def _subscribe_and_handle_responses(self) -> None:
        for topic in self.client_config.get_topics():
            super().subscribe(topic)
            self._add_response_handler(topic)

    def _add_response_handler(self, topic: str) -> None:
        print(f'Checing response handler for "{topic}"')
        if topic == self.__TOPIC_DOOR_ACCESS:
            print(f'Adding response handler for "{topic}"')
            self.message_response_handlers[self.__TOPIC_DOOR_ACCESS] = {
                self.__RESPONSE_CALL_HANDLER: self._handle_message_for_door_access_authorization,
                self.__RESPONSE_CALL_PARSER: MessageParser.DoorAccessMessage,
                self.__RESPONSE_CALL_ACCEPTED: {
                    self.__RESPONSE_CALL_NOW: [self._request_accepted],
                    self.__RESPONSE_CALL_CALLBACKS: [
                        (self._accepted_callback, self.device_reaction_duration), (self.buzzer.off, 0.5)]
                },
                self.__RESPONSE_CALL_DECLINED: {
                    self.__RESPONSE_CALL_NOW: [self._request_declined],
                    self.__RESPONSE_CALL_CALLBACKS: [
                        (self._declined_callback, self.device_reaction_duration), (self.buzzer.off, 1.0)]
                }
            }

    def send_door_access_request(self, rfid_tag: int):
        status = self.authorization_message_statuses[0]
        mac_address = self.client_config.get_mac_address()

        handler = self.message_response_handlers[self.__TOPIC_DOOR_ACCESS]
        super().send(self.__TOPIC_DOOR_ACCESS,
                     handler[self.__RESPONSE_CALL_PARSER].Request.serialize(status, mac_address, rfid_tag))
        self.sent_messages.add(rfid_tag)
