from typing import List
from enum import Enum
from Device.src.utils.utils import get_use_fake_device

if get_use_fake_device():
    from .fake_peripherials.neopixel import NeoPixel
    from  common.fake_config import *
    from .fake_peripherials.my_board import board
else:
    from common.real_config import *
    from neopixel import NeoPixel
    import board as board


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


class _LEDHandler():
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
            self.r, self.g, self.b = rgb

    def __init__(self, diodes: NeoPixel, colors: List[InnerColor]):
        self._diodes = diodes
        self._colors = colors
        self.update_all()

    def update_all(self):
        for i in range(len(self._colors)):
            self._diodes[i] = self._colors[i].rgb
        print(f'LEDs updated to color "{Color(self._colors[0].rgb).name}"')
        self._diodes.show()

    def set_color_all(self, rgb: Color):
        for color in self._colors:
            color.rgb = rgb
        self.update_all()

    def clear(self):
        self.set_color_all(Color.BLACK.value)
        self.update_all()

    def set_green(self):
        self.set_color_all(Color.GREEN.value)
    
    def set_red(self):
        self.set_color_all(Color.RED.value)
        
class LEDHandler(_LEDHandler):
    def __init__(self, brightness=1.0 / 32, auto_write=False):
        super().__init__(
            NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write),
            [self.InnerColor.black() for _ in range(8)])
