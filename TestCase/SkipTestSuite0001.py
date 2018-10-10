import unittest

from appium import webdriver

from library import config, keywords


class C0001(unittest.TestCase):

    __app_path = "http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk"

    @classmethod
    def setUpClass(cls):
        pass
        # print('[SetupClass]')
        # desired_caps = config.GlobalConfig.get_desired_caps()
        # desired_caps['app'] = 'http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk'
        # url = config.GlobalConfig.get_server_url()
        # config.DriverCache.open_app(url, desired_caps)
        # keywords.System.click_ok_if_popup_permission_dialog()
        # print('[SetupClass OK]')

    @classmethod
    def tearDownClass(cls):
        config.DriverCache.close_current()

    def setUp(self):
        pass
        # print('[Setup]')
        # driver = config.DriverCache.current_driver
        # assert isinstance(driver, webdriver.Remote)
        # package = driver.current_package
        # driver.remove_app(package)
        # self.assertFalse(driver.is_app_installed(package))

    def tearDown(self):
        keywords.System.click_ok_if_popup_permission_dialog()

    def test_install_app(self):
        print('[Test Start]')
        # # desired_caps = config.GlobalConfig.get_desired_caps()
        # # if 'app' not in desired_caps:
        # #     desired_caps['app'] = 'http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk'
        # url = config.GlobalConfig.get_server_url()
        # # config.DriverCache.open_app(url, desired_caps)
        # # keywords.current_driver().install_app('http://dlrcs.fetion-portal.com/mobile/RCS_V6.2.4.0930_20180930.apk',
        # #                                       grantPermissions=True)
        # keywords.Android.install_app('http://dlrcs.fetion-portal.com/mobile/RCS_V6.2.4.0930_20180930.apk',
        #                              grantPermissions=True)
        # # keywords.current_driver().switch_to.alert.accept()
        # self.assertTrue(keywords.current_driver().is_app_installed('com.chinasofti.rcs'))

        desired_caps = config.GlobalConfig.get_desired_caps()
        desired_caps['app'] = C0001.__app_path
        url = config.GlobalConfig.get_server_url()
        config.DriverCache.open_app(url, desired_caps)
        self.assertTrue(keywords.current_driver().is_app_installed('com.chinasofti.rcs'))
        print('[Test End]')
