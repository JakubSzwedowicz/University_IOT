from ..utils.utils import use_fake_device

if use_fake_device():
    from .fake_peripherials.my_buzzer import MyBuzzer
    from .fake_peripherials.fake_config import *
else:
    from RPi.GPIO import GPIO
    from Utils.config import *
    class MyBuzzer:
        def __init__(self, pin: int=buzzerPin):
            self.pin = pin
            self._is_on = False

        def on(self):
            self._is_on = True
            GPIO.output(self.pin, False)

        def off(self):
            self._is_on = False
            GPIO.output(self.pin, True)
            
        def is_on(self) -> bool:
            return self._is_on


class BuzzerHandler(MyBuzzer):
    def __init__(self, pin: int=buzzerPin):
        super().__init__(pin)
