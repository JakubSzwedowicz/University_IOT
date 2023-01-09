import random
from enum import Enum
import paho.mqtt.client as mqtt

# from mfrc522 import MFRC522

import RPi.GPIO as GPIO
import neopixel
import board

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


#Fake MFRC522
class MFRC522:
    PICC_REQIDL = "pic_reqidl"
    MI_OK = 0
    MI_ERR = 1

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


class RFIDHandler:
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.is_read = False

    def read(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                if not self.is_read:
                    self.is_read = True
                    return uid
                return None
        else:
            self.is_read = False
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


class LEDHandler:
    class InnerColor:
        def __init__(self, r, g, b, brightness):
            self.r = r
            self.g = g
            self.b = b
            self.brightness = brightness

        @classmethod
        def black(cls):
            return cls(*Color.BLACK.value, 1)

        @property
        def color(self):
            return int(self.r * self.brightness), int(self.g * self.brightness), int(self.b * self.brightness)

        @color.setter
        def color(self, color_tuple):
            self.r, self.g, self.b = color_tuple

    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.__pixels = neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write)
        self.__colors = [self.InnerColor.black() for _ in range(8)]
        self.update_all()

    def update_all(self):
        for i in range(len(self.__colors)):
            self.__pixels[i] = self.__colors[i].color
        self.__pixels.show()

    def set_color_all(self, color_tuple):
        for color in self.__colors:
            color.color = color_tuple
        self.update_all()

    def slow_load(self):
        self.set_rainbow()
        divider = 100
        index = 0
        prev_index = 0
        self.__pixels[index] = self.__colors[index].color
        for i in range(divider * 8 + 2):
            index = int(i / divider)
            if index != prev_index:
                prev_index = index
                self.__pixels[index] = self.__colors[index].color

    def clear(self):
        self.set_color_all(Color.BLACK.value)
        self.update_all()

    def set_rainbow(self):
        self.__colors[0].color = Color.RED.value
        self.__colors[1].color = Color.ORANGE.value
        self.__colors[2].color = Color.YELLOW.value
        self.__colors[3].color = Color.LIME.value
        self.__colors[4].color = Color.GREEN.value
        self.__colors[5].color = Color.CYAN.value
        self.__colors[6].color = Color.BLUE.value
        self.__colors[7].color = Color.PURPLE.value

    def rainbow(self):
        self.set_rainbow()
        self.update_all()


class Buzzer:
    def __int__(self, pin):
        self.pin = pin

    def on(self):
        GPIO.output(self.pin, True)

    def off(self):
        GPIO.output(self.pin, True)