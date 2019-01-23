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
                mobile = self.get_connection(key)
            except:
                mobile = MobileFactory.from_available_devices_setting(key)
                self.register(mobile, key)

            # try:
            download_url = available_devices.TARGET_APP.get('DOWNLOAD_URL')
            if os.environ.get('APP_DOWNLOAD_URL'):
                download_url = os.environ.get('APP_DOWNLOAD_URL')
            # 尝试安装APP
            package = available_devices.TARGET_APP.get('APP_PACKAGE')
            if os.environ.get('APPIUM_INSTALL_APP_ACTION'):
                install_flag = True
            else:
                install_flag = available_devices.TARGET_APP.get('INSTALL_BEFORE_RUN')
            if install_flag:
                self.try_install_app_while_register_mobile(mobile, download_url, package)

    def close_all(self, closer_method='disconnect_mobile'):
        for conn in self._connections:
            getattr(conn, closer_method)()
        return self.current

    @staticmethod
    def try_install_app_while_register_mobile(mobile, download_url, package):
        try:
            mobile.connect_mobile()
        except:
            import traceback
            msg = traceback.format_exc()
            print('手机连接失败，请确认手机配置信息！')
            print(msg)
        mobile.remove_app(package)
        retry = 0
        while True:
            try:
                mobile.install_app(download_url)
                break
            except:
                retry += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)
                if retry > 3:
                    break
                print("尝试为手机安装app期间发生异常！开始重试，重试第{}次".format(retry))
