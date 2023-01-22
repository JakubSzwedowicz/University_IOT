from src.device.real_device import device_handler

if __name__ == '__main__':
    device = device_handler.DeviceHandler()
    device.run()
    
    # rfid_handler = RFIDHandler()
    # pub = Publisher(TOPIC)
    # led = LEDHandler()
    # buzzer = MyBuzzer(buzzerPin)
    # Thread(target=lambda: FakeRFID(rfid_handler.MIFAREReader)).start()
    # buzzer.off()

    # pub.connect()

    # while True:
    #     log_time = datetime.datetime.now()
    #     maybe_uid = rfid_handler.read()
    #     print(f'"{maybe_uid}" at {datetime.datetime.now()}')
    #     if maybe_uid is not None:
    #         message = f'{log_time.hour}:{log_time.minute}:{log_time.second},{log_time.microsecond}'
    #         print(f'RFID card detected at {message}')
    #         led.rainbow()
    #         buzzer.on()
    #         pub.publish(maybe_uid, message)
    #     time.sleep(0.1)
    #     led.clear()
    #     buzzer.off()
