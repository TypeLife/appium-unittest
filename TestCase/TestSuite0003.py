import re
import time
import unittest

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from library import config, keywords, locators
from selenium.webdriver.support import expected_conditions as  EC

from library.elementfinder import ElementFinder


class C0003(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('[SetupClass]')
        desired_caps = config.GlobalConfig.get_desired_caps()
        url = config.GlobalConfig.get_server_url()
        config.DriverCache.open_app(url, desired_caps)
        print('[SetupClass OK]')

    @classmethod
    def tearDownClass(cls):
        config.DriverCache.close_current()

    def setUp(self):
        print('[SetUp]')
        driver = config.DriverCache.current_driver
        assert isinstance(driver, webdriver.Remote)
        self.assertTrue(driver.is_app_installed('com.chinasofti.rcs'))
        keywords.GuidePage.jump_over_the_guide_page()
        keywords.PermissionListPage.accept_all_permission_in_list()
        keywords.PermissionGrantPage.always_allow_popup_permission()
        driver.wait_activity('com.cmcc.cmrcs.android.ui.activities.OneKeyLoginActivity', 3)
        print('[SetUp OK]')

    def tearDown(self):
        pass

    def test_one_key_login(self):
        print('[Test Start]')
        driver = config.DriverCache.current_driver
        assert isinstance(driver, webdriver.Remote)
        WebDriverWait(driver, 8).until(lambda d: re.fullmatch('\d{11}', ElementFinder.find_element(
            locators.p_login_m_one_key_e_phone_number).text))
        ElementFinder.find_element(locators.p_login_m_one_key_e_one_key_login).click()
        driver.wait_activity('com.cmcc.cmrcs.android.ui.activities.HomeActivity', 5)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locators.p_home_m_footer_e_message))
        print('[Test OK]')
