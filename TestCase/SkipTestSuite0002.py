import unittest

from library import config, keywords


class C0002(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('[SetupClass]')
        desired_caps = config.GlobalConfig.get_desired_caps()
        if 'app' not in desired_caps:
            desired_caps['app'] = 'http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk'
        url = config.GlobalConfig.get_server_url()
        config.DriverCache.open_app(url, desired_caps)
        keywords.System.click_ok_if_popup_permission_dialog()
        print('[SetupClass OK]')

    @classmethod
    def tearDownClass(cls):
        config.DriverCache.close_current()

    def setUp(self):
        print('[SetUp]')
        self.assertTrue(keywords.current_driver().is_app_installed('com.chinasofti.rcs'))
        print('[SetUp OK]')

    def tearDown(self):
        print('[Teardown]')
        desired_caps = config.GlobalConfig.get_desired_caps()
        if 'app' not in desired_caps:
            desired_caps['app'] = 'http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk'
        url = config.GlobalConfig.get_server_url()
        config.DriverCache.open_app(url, desired_caps)
        keywords.System.click_ok_if_popup_permission_dialog()
        # keywords.current_driver().install_app('http://dlrcs.fetion-portal.com/mobile/RCS_V6.2.4.0930_20180930.apk')
        # keywords.System.click_ok_if_popup_permission_dialog()
        print('[Teardown OK]')

    def test_remove_app(self):
        print('[Test Start]')
        # driver = config.DriverCache.current_driver
        # assert isinstance(driver, webdriver.Remote)
        package = keywords.current_driver().current_package
        keywords.current_driver().remove_app(package)
        self.assertFalse(keywords.current_driver().is_app_installed(package))
        print('[Test OK]')
