from abc import ABCMeta, abstractmethod
from typing import Optional
from ..utils.utils import use_fake_device

if use_fake_device():
    from .fake_device.device_handler import DeviceHandler as DeviceHandlerImpl
else:
    from .real_device.device_handler import DeviceHandler as DeviceHandlerImpl
    
DeviceHandler = DeviceHandlerImpl