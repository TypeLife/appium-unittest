import unittest

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

from library import config, keywords

p_welcome_m_main_e_start_to_use = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageButton")')
p_login_m_form_e_account = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").index(0)')
p_login_m_form_e_password = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").index(1)')


class Demo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        desired_caps = config.GlobalConfig.get_desired_caps()
        url = config.GlobalConfig.get_server_url()
        config.DriverCache.open_app(url, desired_caps)

    @classmethod
    def tearDownClass(cls):
        config.DriverCache.close_current()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_demo_01(self):
        driver = config.DriverCache.current_driver
        assert isinstance(driver, webdriver.Remote)
        keywords.GuidePage.jump_over_the_guide_page()
        keywords.PermissionListPage.accept_all_permission_in_list()
        keywords.PermissionGrantPage.always_allow_popup_permission()
        self.assertEqual(1, 1)
