from abc import ABCMeta, abstractmethod
from paho.mqtt.client import Client, MQTTMessage
from typing import Tuple

class _Serializer():
    @staticmethod
    @abstractmethod
    def serialize(*args, **kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(*args, **kwargs) -> tuple:
        pass
class _IMessage():
    class Request(_Serializer):
        pass
        
    class Response(_Serializer):
        pass
        
class MessageParser:
    class DoorAccessMessage(_IMessage):
        class _RequestResponseImpl:
            @staticmethod
            def serialize(authorization_message_status: str, mac_address: str, rfid_tag: int) -> str:
                print(f'Serialize: {authorization_message_status}, {mac_address}, {rfid_tag}')
                return f'{authorization_message_status};{mac_address};{rfid_tag}'
                
            @staticmethod
            def deserialize(message: MQTTMessage) -> Tuple[str, str, int]:
                '''DatabaseData.Definitions.AuthorizationMessageStatus, DatabaseData.Definitions.Device, DatabaseData.Definitions.Card'''
                status, mac_address, rfid_tag = str(message.payload.decode('utf-8')).split(';')
                print(f'Deserialize: {status}, {mac_address}, {rfid_tag}')
                return (status, mac_address, rfid_tag)
            
        class Request(_RequestResponseImpl):
            pass
        
        class Response(_RequestResponseImpl):
            pass

class Connection:
    def __init__(self, ip_address: str, port: int, on_message_callback):
        self.ip_address = ip_address
        self.port = port
        self.client = Client()
        self.client.on_message = on_message_callback

        # import logging
        # logging.basicConfig(level=logging.DEBUG)
        # logger = logging.getLogger(__name__)
        # self.client.enable_logger(logger)

    def connect(self):
        print(f'Connecting to {self.ip_address}:{self.port}')
        self.client.connect(host=self.ip_address, port=self.port)
        self.client.loop_start()

    def disconnect(self):
        print(f'Disconnecting from {self.ip_address}:{self.port}')
        self.client.disconnect()
        self.client.loop_stop()

    def send(self, topic: str, message: str):
        print(f'Sending message "{message}" under topic "{topic}"')
        self.client.publish(topic, message)
        
class IPublisherSubscriber(Connection):
    def __init__(self, ip_address: str, port: int, on_message_callback: callable):
        super().__init__(ip_address, port, on_message_callback)
        print('Setting on_message callback')

    def connect(self):
        super().connect()

    def subscribe(self, topic: str):
        print(f'Subscribed to topic "{topic}"')
        self.client.subscribe(topic)
        
    @abstractmethod
    def process_message(client, userdata, message: MQTTMessage):
        pass
