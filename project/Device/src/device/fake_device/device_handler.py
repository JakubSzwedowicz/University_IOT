import tkinter as tk
import json

from ..real_device.device_handler import DeviceHandler as RealDeviceHandler
from ...peripherials.leds_handler import LEDHandler
from ...peripherials.buzzer_handler import BuzzerHandler

class DeviceHandler(RealDeviceHandler):
    def __init__(self):
        super().__init__()
        window = tk.Tk()
        window.geometry("200x200")
        grid = tk.Frame(window)
    
        # self._change_runnable(self._run)
        
        self.connected = False        

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
        
        led_circle = tk.Canvas(grid, width=50, height=50, bg='white')
        led_circle.grid(row=0, column=1)
        led_circle.create_oval(5, 5, 45, 45, fill='white')
        led_circle.bind('<<LED_GREEN>>', lambda event=None: led_circle.itemconfig(1, fill='green'))
        led_circle.bind('<<LED_RED>>', lambda event=None: led_circle.itemconfig(1, fill='red'))
        led_circle.bind('<<LED_CLEAR>>', lambda event=None: led_circle.itemconfig(1, fill='white'))
                  
        # Create another button and place it in the (1, 0) position
        button_iterate = tk.Button(grid, text="run loop")
        button_iterate.grid(row=1, column=0)
        button_iterate.bind('<ButtonPress-1>', lambda event=None: self.run())
                  
        buzzer_circle = tk.Canvas(grid, width=50, height=50, bg='white')
        buzzer_circle.grid(row=1, column=1)
        buzzer_circle.create_oval(5, 5, 45, 45, fill='white')
        buzzer_circle.bind('<<BUZZER_ON>>', lambda event=None: buzzer_circle.itemconfig(1, fill='yellow'))
        buzzer_circle.bind('<<BUZZER_OFF>>', lambda event=None: buzzer_circle.itemconfig(1, fill='white'))
                  
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        # button_attach.after(1000, self.main_loop)
        
        self.led = _LedHandlerWrapper(led_circle, self.led)
        self.buzzer = _BuzzerHandlerWrapper(buzzer_circle, self.buzzer)
        
        window.mainloop()

    def switch_successful(self):
        self.RFID_handler.MIFAREReader.switch_succesful()
        
    def set_successful(self, succ=True):
        print(succ)
        self.RFID_handler.MIFAREReader.set_successful(succ)
        
      
    def run(self):
        print(30*'=' + '\nNext iteration of fake DeviceHandler...')
        try:
            if not self.connected:
                self.connect()
                self._subscribe_and_handle_responses()
                self.connected = True
            self.main_loop()
        except KeyboardInterrupt as ex:
            print(f'KeyboardInterrupt: "{ex}"')
        
        
        
class _LedHandlerWrapper(LEDHandler):
    def __init__(self, led_circle: tk.Canvas, *args, **kwargs):
        if isinstance(args[0], LEDHandler):
            self.__dict__ = args[0].__dict__.copy()
            args = args[1:]
        else:
            super().__init__(*args, **kwargs)
        self.led_circle = led_circle
        
    def set_green(self):
        print(f'LedWrapper set to "green"')
        self.led_circle.event_generate('<<LED_GREEN>>')
        return super().set_green()
    
    def set_red(self):
        print(f'LedWrapper set to "red"')
        self.led_circle.event_generate('<<LED_RED>>')
        return super().set_red()
    
    def clear(self):
        self.led_circle.event_generate('<<LED_CLEAR>>')
        return super().clear()
    
    
class _BuzzerHandlerWrapper(BuzzerHandler):
    def __init__(self, buzzer_circle: tk.Canvas, *args, **kwargs):
        if isinstance(args[0], BuzzerHandler):
            self.__dict__ = args[0].__dict__.copy()
            args = args[1:]
        else:
            super().__init__(*args, **kwargs)
        self.buzzer_circle = buzzer_circle
                    
    def on(self):
        print(f'BuzzerWrapper set to "on"')
        self.buzzer_circle.event_generate('<<BUZZER_ON>>')
        return super().on()

    def off(self):
        print(f'BuzzerWrapper set to "off"')
        self.buzzer_circle.event_generate('<<BUZZER_OFF>>')
        return super().off()
    