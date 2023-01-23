from .src.device import device_handler

def main():
    device = device_handler.DeviceHandler()
    device.run()

if __name__ == '__main__':
    main()
