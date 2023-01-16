from datetime import datetime
from enum import Enum 
from typing import List, Callable, Tuple


from config import *
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time
import neopixel
import board
import busio
import w1thermsensor
import adafruit_bme280.advanced as adafruit_bme280
from mfrc522 import MFRC522
import lib.oled.SSD1331 as SSD1331


Point2D = Tuple[int, int]
Vector2D = List[Point2D]

def format_date(time: datetime) -> str:
        return f'{time.hour}:{time.minute}:{time.second},{time.microsecond}'

class Font:
    ARIAL = ImageFont.truetype("fonts/arial.ttf")
    TIMES = ImageFont.truetype("fonts/times.ttf")
    MATORAN = ImageFont.truetype("fonts/Matoran.ttf")

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
    
class OLEDHandler:
    def __init__(self, image_color: Color, image_filename):
        self.__disp = SSD1331.SSD1331()
        self.__disp.Init()
        self.__disp.clear()
        self.__image = Image.open(image_filename)
        self.__draw = ImageDraw.Draw(self.__image)
        self.__background_color = image_color

    def show(self):
        self.__disp.ShowImage(self.__image)

    def clear_whole_display(self):
        self.__disp.clear()

    def reset(self):
        self.__disp.reset()

    def width(self):
        return self.__disp.width

    def height(self):
        return self.__disp.height

    # PRINTS --------------------------------------------------------
    def draw(self, starting_point: Point2D, text: str, color: Color=None, font:Font=Font.ARIAL):
        self.__draw.text(starting_point, text, fill=color, font=font)

    # CLEAR ---------------------------------------------------------
    def clear_on_rectangle_diagonal(self, rectangle_diagonal: Vector2D):
        self.__draw.rectangle(rectangle_diagonal, fill=self.__background_color)


class BME280Handler:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        self.__bme280.sea_level_preasure = 1013.25
        self.__bme280.standby_period = adafruit_bme280.STANDBY_TC_500
        self.__bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.__bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.__bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.__bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2


    def temperature(self):
        return self.__bme280.temperature

    def altitude(self):
        return self.__bme280.altitude

    def pressure(self):
        return self.__bme280.pressure

    def humidity(self):
        return self.__bme280.humidity


class Task_1:
    TEMPERATURE_STEP = 0.1
    HUMIDITY_STEP = 0.1
    ALTITUDE_STEP = 0.1
    PRESSURE_STEP = 1
    PIXEL_RIGHT = 30
    RIGHTEST_PIXEL_INDEX = 95

    def __init__(self):
        self.oled_handler = OLEDHandler(Color.GREY.value, "images/background_dark.png")
        self.bme280 = BME280Handler()
        self.handlers = \
            [
                self.SensorHandler(self.oled_handler, self.bme280.temperature,
                                   (self.PIXEL_RIGHT, 3),
                                   ((self.PIXEL_RIGHT, 0), (self.RIGHTEST_PIXEL_INDEX, 20)),
                                   self.TEMPERATURE_STEP, 'Temp:', 'C'),
                self.SensorHandler(self.oled_handler, self.bme280.humidity,
                                   (self.PIXEL_RIGHT, 19),
                                   ((self.PIXEL_RIGHT, 15), (self.RIGHTEST_PIXEL_INDEX, 35)),
                                   self.HUMIDITY_STEP, 'Hum:', '%'),
                self.SensorHandler(self.oled_handler, self.bme280.altitude,
                                   (self.PIXEL_RIGHT, 35),
                                   ((self.PIXEL_RIGHT, 30), (self.RIGHTEST_PIXEL_INDEX, 50)),
                                   self.ALTITUDE_STEP, 'Alt:', 'm'),
                self.SensorHandler(self.oled_handler, self.bme280.pressure,
                                   (self.PIXEL_RIGHT, 50),
                                   ((self.PIXEL_RIGHT, 45), (self.RIGHTEST_PIXEL_INDEX, 65)),
                                   self.PRESSURE_STEP, 'Press:', 'hPa')
            ]

    def print_all(self):
        for handler in self.handlers:
            handler.draw()
        self.oled_handler.show()

    class SensorHandler:

        def __init__(self, oled_handler: OLEDHandler, value_source:Callable, starting_pixel:Point2D, clearing_rectangle_diagonal: Vector2D, value_step, extra_text: str, unit: str):
            self.oled_handler = oled_handler
            self.value_source = value_source
            self.current_value = -value_source()
            self.starting_pixel = starting_pixel
            self.clearing_rectangle_diagonal = clearing_rectangle_diagonal
            self.value_step = value_step
            self.extra_text = extra_text
            self.unit = unit

        def draw(self, font:Font=Font.ARIAL, color: Color=None):
            new_value = self.value_source()
            if abs(self.current_value - new_value) > self.value_step:
                self.current_value = new_value
                self.oled_handler.clear_on_rectangle_diagonal(self.clearing_rectangle_diagonal)
                text = f'{self.extra_text} {round(self.current_value, 1)} {self.unit}'
                self.oled_handler.draw(self.starting_pixel, text, color=color, font=font)

class LedController:
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


class RFIDHandler:
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.start_time = None
        self.prev_status = 2
        self.is_read = False

    def read(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        print(f'Status value: {status}, prev_status: {self.prev_status}, is_read: {self.is_read}')
        if not self.is_read:
            if status == self.MIFAREReader.MI_OK and self.prev_status != self.MIFAREReader.MI_OK:
                self.is_read = True
                (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
                if status == self.MIFAREReader.MI_OK:
                    print(f'DEBUG PRINT 0:{uid[0]}, type:{type(uid[0])} size:{len(uid)}')
                    self.start_time = datetime.now()
                    self.prev_status = status
                    return True
        elif status == self.MIFAREReader.MI_ERR and self.prev_status == self.MIFAREReader.MI_ERR:
            self.is_read = False
        self.prev_status = status
        return False


    def __str__(self):
        print(f'Is card sensed: {self.is_being_sensed}; Last card read time: {PrettyDate.to_str(self.start_time)}')


class Buzzer:
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        GPIO.output(self.pin, False)
        
    def off(self):
        GPIO.output(self.pin, True)


class Task_2:
    def __init__(self):
        self.rfidh = RFIDHandler()
        self.led = LedController()
        self.signal_time_period = 1
        self.buzzer = Buzzer(buzzerPin)

    def run(self):
        is_read = self.rfidh.read()
        if is_read:
            print(self.rfidh)
            self.buzzer.on()
            self.led.rainbow()

        if self.rfidh.start_time + self.signal_time_period < datetime.now():
            self.buzzer.off()

        if not self.rfidh.is_being_sensed:
            self.led.set_color_all(Color.black)


if __name__ == '__main__':
    # task_1 = Task_1()
    task_2 = Task_2()
    while True:
        # task_1.print_all()
        task_2.run()
