class MyBuzzer:
    def __init__(self, pin: int=0):
        self.pin = pin
        self._is_on = False

    def on(self):
        self._is_on = True

    def off(self):
        self._is_on = False
        
    def is_on(self) -> bool:
        return self._is_on
