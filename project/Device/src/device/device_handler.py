from ..utils.utils import get_use_fake_device

if get_use_fake_device():
    from .fake_device.device_handler import DeviceHandler as DeviceHandlerImpl
else:
    from .real_device.device_handler import DeviceHandler as DeviceHandlerImpl
    
DeviceHandler = DeviceHandlerImpl