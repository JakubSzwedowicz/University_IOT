from random import randint

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
            return self.MI_OK, f'{randint(0, 10000)}'
        return self.MI_ERR, "exampleUid"