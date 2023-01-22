import tkinter as tk
import json

from ..real_device.device_handler import DeviceHandler as RealDeviceHandler
from src.peripherials.leds_handler import LEDHandler
from src.peripherials.buzzer_handler import BuzzerHandler

class DeviceHandler(RealDeviceHandler):
    def __init__(self):
        super().__init__()
        self.led_wrapper = _LedHandlerWrapper(self.led)
        self.buzzer_wrapper = _BuzzerHandlerWrapper(self.buzzer)
        self._change_runnable(self._run)
        
        self.connected = False
        
        
        window = tk.Tk()
        # window.geometry("200x200")
        grid = tk.Frame(window)
        grid.grid(sticky="nsew", padx=10, pady=10)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)
        
        window.title("Device simulator")

        button_attach = tk.Button(grid, text="ATTACH CARD")
        button_attach.grid(row=0, column=0)
        button_attach.bind('<ButtonPress-1>', lambda event=None: self.switch_successful())
        # button_attach.bind('<ButtonRelease-1>', lambda event=None: self.set_success(False))
        
        circle = tk.Canvas(grid, width=50, height=50, bg='white')
        circle.grid(row=0, column=1)
        circle.create_oval(5, 5, 45, 45, fill='white')
        circle.bind('<<LED_GREEN>>', lambda event=None: circle.itemconfig(1, fill='green'))
        circle.bind('<<LED_RED>>', lambda event=None: circle.itemconfig(1, fill='red'))
        circle.bind('<<LED_CLEAR>>', lambda event=None: circle.itemconfig(1, fill='white'))
                  
        # Create another button and place it in the (1, 0) position
        button_iterate = tk.Button(grid, text="run loop")
        button_iterate.grid(row=1, column=0)
        button_iterate.bind('<ButtonPress-1>', lambda event=None: self._runnable())
                  
        buzzer = tk.Canvas(grid, width=50, height=50, bg='white')
        buzzer.grid(row=1, column=1)
        buzzer.create_oval(5, 5, 45, 45, fill='white')
        buzzer.bind('<<BUZZER_ON>>', lambda event=None: circle.itemconfig(1, fill='black'))
        buzzer.bind('<<BUZZER_OFF>>', lambda event=None: circle.itemconfig(1, fill='white'))
                  
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        # button_attach.after(1000, self.main_loop)
        window.mainloop()

    def switch_successful(self):
        self.RFID_handler.MIFAREReader.switch_succesful()
        
    def set_successful(self, succ=True):
        print(succ)
        self.RFID_handler.MIFAREReader.set_successful(succ)
        
      
    def _run(self):
        print('It works!')
        if not self.connected:
            self.connect()
            self.connected = True
        self.main_loop()
        
        
        
class _LedHandlerWrapper(LEDHandler):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0], LEDHandler):
            self.__dict__ = args[0].__dict__.copy()
            args = args[1:]
        else:
            super().__init__(*args, **kwargs)
        
    def set_green(self):
        print(f'LedWrapper set to "green"')
        tk.event_generate('<<LED_GREEN>>')
        return super().set_green()
    
    def set_red(self):
        print(f'LedWrapper set to "red"')
        tk.event_generate('<<LED_RED>>')
        return super().set_red()
    
    def clear(self):
        tk.event_generate('<<LED_CLEAR>>')
        return super().clear()
    
    
class _BuzzerHandlerWrapper(BuzzerHandler):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0], BuzzerHandler):
            self.__dict__ = args[0].__dict__.copy()
            args = args[1:]
        else:
            super().__init__(*args, **kwargs)
            
    def set_on(self):
        print(f'BuzzerWrapper set to "on"')
        tk.event_generate('<<BUZZER_ON>>')
        return super().set_on()

    def set_off(self):
        print(f'BuzzerWrapper set to "off"')
        tk.event_generate('<<BUZZER_OFF>>')
        return super().set_off()
    