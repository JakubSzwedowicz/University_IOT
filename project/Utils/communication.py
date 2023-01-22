from abc import ABCMeta, abstractmethod
from paho.mqtt.client import Client, MQTTMessage
from typing import Tuple

# from mfrc522 import MFRC522

from database.scripts.utils import DatabaseData

class _Serializer(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def serialize(*args, **kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(*args, **kwargs) -> tuple:
        pass
class _IMessage(metaclass=ABCMeta):
    class Request(metaclass=_Serializer):
        pass
        
    class Response(metaclass=_Serializer):
        pass
        
class MessageParser:
    class DoorAccessMessage(metaclass=_IMessage):
        class _RequestResponseImpl:
            @staticmethod
            def serialize(authorization_message_status: str, mac_address: str, rfid_tag: int) -> str:
                return f'{authorization_message_status};{mac_address};{rfid_tag}'
                
            @staticmethod
            def deserialize(message: MQTTMessage) -> Tuple[DatabaseData.Definitions.AuthorizationMessageStatus, DatabaseData.Definitions.Device, DatabaseData.Definitions.Card]:
                status, mac_address, rfid_tag = str(message.payload.decode('utf-8')).split(';')
                return (status, mac_address, rfid_tag)
            
        class Request(_RequestResponseImpl):
            pass
        
        class Response(_RequestResponseImpl):
            pass

TOPICS = {
    'authorization/door_access' : MessageParser.DoorAccessMessage
}
  
class Connection:
    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port
        self.client = Client()

    def connect(self):
        self.client.connect(host=self.ip_address, port=self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect(host=self.ip_address, port=self.port)
        self.client.loop_stop()

    def send(self, topic: str, message: str):
        self.client.publish(topic, message)
        
class IPublisherSubscriber(Connection, ABCMeta):
    def __init__(self, ip_address: str, port: int, on_message_callback: callable):
        super().__init__(ip_address, port)
        self.client.on_message = on_message_callback

    def connect(self):
        super().connect()

    def subscribe(self, topic: str):
        self.client.subscribe(topic)
        
    @abstractmethod
    def process_message(client, userdata, message: MQTTMessage):
        pass

class Subscriber(Connection):
    def __init__(self):
        super().__init__()

    def connect(self):
        super().connect()
        self.client.on_message = self.process_message
        self.client.loop_start()

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def process_message(client, userdata, message: MQTTMessage):
        card_uid, log_time = str(message.payload.decode('utf-8')).split(';')
        print(f'Received: "{card_uid}" registered at: "{log_time}"')