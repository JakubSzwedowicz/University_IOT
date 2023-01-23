from configparser import ConfigParser
from Device.src.utils.utils import get_use_fake_device

if get_use_fake_device():
    print('Using fake devices...')
else:
    print('Using real devices')
