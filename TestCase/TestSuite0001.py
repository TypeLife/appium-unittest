import unittest

from appium import webdriver

from library import config, keywords


class C0001(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('[SetupClass]')
        desired_caps = config.GlobalConfig.get_desired_caps()
        desired_caps['app'] = 'http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk'
        url = config.GlobalConfig.get_server_url()
        config.DriverCache.open_app(url, desired_caps)
        keywords.System.click_ok_if_popup_permission_dialog()
        print('[SetupClass OK]')

    @classmethod
    def tearDownClass(cls):
        config.DriverCache.close_current()

    def setUp(self):
        print('[Setup]')
        driver = config.DriverCache.current_driver
        assert isinstance(driver, webdriver.Remote)
        package = driver.current_package
        driver.remove_app(package)
        self.assertFalse(driver.is_app_installed(package))

    def tearDown(self):
        keywords.System.click_ok_if_popup_permission_dialog()

    def test_install_app(self):
        print('[Test Start]')
        driver = config.DriverCache.current_driver
        assert isinstance(driver, webdriver.Remote)
        driver.install_app('http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk')
        self.assertTrue(driver.is_app_installed('com.chinasofti.rcs'))
        print('[Test End]')
