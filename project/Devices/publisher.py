import time
import datetime
import tkinter
from typing import Dict, List
from threading import Thread

from Utils.config import *
from Utils.common import Connection, RFIDHandler, TOPIC, MyBuzzer, ILEDHandler, MFRC522


class DevicesEmulator:
    def __init__(self, card_reader_with_leds: Dict[MFRC522, List[ILEDHandler]]) -> None:
        

class FakeRFID:
    def __init__(self, mfrc: MFRC522):
        self.mfrc = mfrc
        window = tkinter.Tk()
        window.title("SENDER")

        button_attach = tkinter.Button(window, text="ATTACH CARD"
                                       # , command=lambda event=None: self.card_reader.successful
                                       )
        button_attach.bind('<ButtonPress-1>', lambda event=None, succ=True: self.set_success(succ))
        button_attach.bind('<ButtonRelease-1>', lambda event=None, succ=False: self.set_success(succ))
        button_attach.grid(row=0, column=0)
        window.mainloop()

    def set_success(self, succ=True):
        print(succ)
        self.mfrc.successful = succ


class Publisher(Connection):
    def __init__(self, topic: str):
        super().__init__()
        self.topic = topic

    def publish(self, card_id: int, log_time: str):
        self.send(self.topic, str(card_id) + ';' + log_time)


if __name__ == '__main__':
    rfid_handler = RFIDHandler()
    pub = Publisher(TOPIC)
    led = LEDHandler()
    buzzer = MyBuzzer(buzzerPin)
    # Thread(target=lambda: FakeRFID(rfid_handler.MIFAREReader)).start()
    buzzer.off()

    pub.connect()

    while True:
        log_time = datetime.datetime.now()
        maybe_uid = rfid_handler.read()
        print(f'"{maybe_uid}" at {datetime.datetime.now()}')
        if maybe_uid is not None:
            message = f'{log_time.hour}:{log_time.minute}:{log_time.second},{log_time.microsecond}'
            print(f'RFID card detected at {message}')
            led.rainbow()
            buzzer.on()
            pub.publish(maybe_uid, message)
        time.sleep(0.1)
        led.clear()
        buzzer.off()

