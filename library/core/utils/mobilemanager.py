import os

from library.core.mobilefactory import MobileFactory
from .connectioncache import ConnectionCache

ENVIRONMENT_VARIABLE = 'AVAILABLE_DEVICES_SETTING'


class MobileManager(ConnectionCache):
    def __init__(self):
        super(MobileManager, self).__init__()
        self.init_mobile_resource()

    def init_mobile_resource(self):
        from settings import available_devices
        devices_setting_value = os.environ.get(ENVIRONMENT_VARIABLE)
        if devices_setting_value:
            devices_setting_value = getattr(available_devices, devices_setting_value, None)
        else:
            devices_setting_value = available_devices.AVAILABLE_DEVICES
        for key in devices_setting_value.keys():
            try:
                self.get_connection(key)
            except:
                mobile = MobileFactory.from_available_devices_setting(key)
                self.register(mobile, key)

    def close_all(self, closer_method='disconnect_mobile'):
        for conn in self._connections:
            getattr(conn, closer_method)()
        return self.current
