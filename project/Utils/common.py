import random
from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import List, Optional
import paho.mqtt.client as mqtt

# from mfrc522 import MFRC522

import RPi.GPIO as GPIO
import neopixel
import board

# TODO: Move to the 'Devices' in the future 
TOPIC = 'id/card'


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    LIME = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    SILVER = (192, 192, 192)
    GREY = (128, 128, 128)
    MAROON = (128, 0, 0)
    OLIVE = (128, 128, 0)
    GREEN = (0, 128, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)
    NAVY = (0, 0, 128)
    ORANGE = (255, 128, 0)


# Fake MFRC522
class MFRC522:
    PICC_REQIDL = "pic_reqidl"
    MI_OK = 0
    MI_ERR = 1
    MI_NOTAGGER = 2

    def __init__(self, successful=False):
        self.successful = successful

    def MFRC522_Request(self, arg):
        if self.successful:
            return self.MI_OK, "exampleTag"
        return self.MI_ERR, "exampleTag"

    def MFRC522_Anticoll(self):
        if self.successful:
            return self.MI_OK, f'{random.randint(0, 10000)}'
        return self.MI_ERR, "exampleUid"


class IRFIDHandler(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Optional[int]:
        pass


class RFIDHandler(IRFIDHandler):
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.prev_status = self.MIFAREReader.MI_NOTAGGER
        self.is_read = False

    def read(self) -> Optional[int]:
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        print(f'Status value: {status}, prev_status: {self.prev_status}, is_read: {self.is_read}')
        if not self.is_read:
            if status == self.MIFAREReader.MI_OK and self.prev_status != self.MIFAREReader.MI_OK:
                self.is_read = True
                (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
                if status == self.MIFAREReader.MI_OK:
                    print(f'DEBUG PRINT 0:{uid[0]}, type:{type(uid[0])} size:{len(uid)}')
                    self.prev_status = status
                    return uid[0]
        # elif status == self.MIFAREReader.MI_ERR and self.prev_status == self.MIFAREReader.MI_ERR:
        elif status == self.MIFAREReader.MI_NOTAGGER and self.prev_status == self.MIFAREReader.MI_NOTAGGER:
            self.is_read = False
        self.prev_status = status
        return None


class Connection:
    def __init__(self):
        self.broker = 'localhost'
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker)

    def disconnect(self):
        self.client.disconnect(self.broker)

    def send(self, topic: str, message: str):
        self.client.publish(topic, message)

class neopixel:
    class NeoPixel:
        def __init__(self, board: board, number_of_diodes: int, brightness: float, auto_write: bool) -> None:
            self.board = board
            self.number_of_diodes = number_of_diodes
            self.brightness = brightness
            self.auto_write = auto_write
            self.diodes: int = [i for i in range(number_of_diodes)]

        def __getitem__(self, index: int) -> int:
            return self.diodes[index]

class board:
    class D18:
        def __init__(self) -> None:
            pass


class ILEDHandler(metaclass=ABCMeta):
    class InnerColor:
        def __init__(self, r, g, b, brightness: float):
            if not 0 <= brightness <= 1.0:
                raise ValueError(f'Invalid value for brightness: "{brightness}"')
            self.r = r
            self.g = g
            self.b = b
            self.brightness = brightness

        @classmethod
        def black(cls):
            return cls(*Color.BLACK.value, 1.0)

        @property
        def rgb(self):
            return int(self.r * self.brightness), int(self.g * self.brightness), int(self.b * self.brightness)

        @rgb.setter
        def rgb(self, rgb: Color):
            self.r, self.g, self.b = rgb.value

    def __init__(self, diodes: neopixel.NeoPixel, colors: List[InnerColor]):
        self._diodes = diodes
        self._colors = colors
        self.update_all()
        pass

    def update_all(self):
        for i in range(len(self._colors)):
            self._diodes[i] = self._colors[i].rgb
        self._diodes.show()

    def set_color_all(self, rgb: Color):
        for color in self.__colors:
            color.rgb = rgb
        self.update_all()

    def clear(self):
        self.set_color_all(Color.BLACK.value)
        self.update_all()

    def set_rainbow(self):
        self._colors[0].rgb = Color.RED.value
        self._colors[1].rgb = Color.ORANGE.value
        self._colors[2].rgb = Color.YELLOW.value
        self._colors[3].rgb = Color.LIME.value
        self._colors[4].rgb = Color.GREEN.value
        self._colors[5].rgb = Color.CYAN.value
        self._colors[6].rgb = Color.BLUE.value
        self._colors[7].rgb = Color.PURPLE.value

    def rainbow(self):
        self.set_rainbow()
        self.update_all()


class LEDHandler(ILEDHandler):
    def __init__(self, brightness=1.0 / 32, auto_write=False):
        super().__init__(
            neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write),
            [self.InnerColor.black() for _ in range(8)])

    def slow_load(self):
        self.set_rainbow()
        divider = 100
        index = 0
        prev_index = 0
        self.__diodes[index] = self.__colors[index].rgb
        for i in range(divider * 8 + 2):
            index = int(i / divider)
            if index != prev_index:
                prev_index = index
                self.__diodes[index] = self.__colors[index].rgb


class MyBuzzer:
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        GPIO.output(self.pin, False)

    def off(self):
        GPIO.output(self.pin, True)


