from configparser import ConfigParser
from ..utils.utils import use_fake_device

if use_fake_device():
    print('Using fake devices...')
else:
    print('Using real devices')
