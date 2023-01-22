from abc import ABCMeta, abstractmethod
from typing import Optional
from ..utils.utils import use_fake_device

if use_fake_device():
    from .fake_peripherials.card_reader import MFRC522
    from .fake_peripherials.fake_config import *
else:
    from Utils.config import *
    from mfrc522 import MFRC522


class IRFIDHandler(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Optional[int]:
        pass


class RFIDHandler(IRFIDHandler):
    def __init__(self):
        super().__init__()
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