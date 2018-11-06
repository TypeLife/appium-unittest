from library.core.mobilefactory import MobileFactory
from .connectioncache import ConnectionCache


class MobileManager(ConnectionCache):
    def __init__(self):
        super(MobileManager, self).__init__()
        self.init_mobile_resource()

    def init_mobile_resource(self):
        from settings.available_devices import AVAILABLE_DEVICES
        for key in AVAILABLE_DEVICES.keys():
            # if not self.get_connection(key):
            try:
                self.get_connection(key)
            except:
                mobile = MobileFactory.from_available_devices_setting(key)
                self.register(mobile, key)

    def close_all(self, closer_method='disconnect_mobile'):
        super(MobileManager, self).close_all()
