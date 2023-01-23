from ..utils.utils import get_use_fake_device

if get_use_fake_device():
    from .fake_peripherials.my_buzzer import MyBuzzer
    from common.fake_config import *
else:
    from RPi.GPIO import GPIO
    from common.real_config import *
    
    class MyBuzzer:
        def __init__(self, pin: int=buzzerPin):
            self.pin = pin
            self._is_on = False

        def on(self):
            print(f'Buzzer set to on')
            self._is_on = True
            GPIO.output(self.pin, False)

        def off(self):
            print(f'Buzzer set to off')
            self._is_on = False
            GPIO.output(self.pin, True)
            
        def is_on(self) -> bool:
            return self._is_on


class BuzzerHandler(MyBuzzer):
    def __init__(self, pin: int=buzzerPin):
        super().__init__(pin)
