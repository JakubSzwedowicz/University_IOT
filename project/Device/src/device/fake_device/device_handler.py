from tkinter import Tk, Button
import json

from ..real_device.device_handler import DeviceHandler as RealDeviceHandler

class DeviceHandler(RealDeviceHandler):
    def __init__(self, config_path: str = CLIENT_CONFIG_PATH):
        window = Tk()
        window.title("SENDER")

        button_attach = Button(window, text="ATTACH CARD"
                                    # , command=lambda event=None: self.card_reader.successful
                                    )
        button_attach.bind('<ButtonPress-1>', lambda event=None,
                        succ=True: self.set_success(succ))
        button_attach.bind('<ButtonRelease-1>', lambda event=None,
                        succ=False: self.set_success(succ))
        button_attach.grid(row=0, column=0)
        window.mainloop()

    def set_success(self, succ=True):
        print(succ)
        self.mfrc.successful = succ