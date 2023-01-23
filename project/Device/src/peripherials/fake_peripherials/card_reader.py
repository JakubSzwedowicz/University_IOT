from random import randint


class MFRC522:
    PICC_REQIDL = "pic_reqidl"
    MI_OK = 0
    MI_ERR = 1
    MI_NOTAGGER = 2

    def __init__(self, successful: bool = False):
        self.successful = successful
        self.rfid = None

    def MFRC522_Request(self, arg):
        if self.successful:
            return self.MI_OK, "exampleTag"
        return self.MI_NOTAGGER, "exampleTag"

    def MFRC522_Anticoll(self):
        if self.successful:
            return self.MI_OK, (f'{randint(0, 10000)}' if self.rfid is None else self.rfid)
        return self.MI_NOTAGGER, "exampleUid"

    def switch_succesful(self):
        self.set_successful(not self.successful)
        
    def set_successful(self, successful):
        print(f'Setting MFRC522.successful to "{successful}"')
        self.successful = successful

    def set_rfid(self, rfid: int):
        print(f'Setting MFRC522.rfid to "{rfid}"')
        self.rfid = rfid
