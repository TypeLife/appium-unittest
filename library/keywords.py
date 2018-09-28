import re

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait

from library.elementfinder import ElementFinder
from library import config
from appium import webdriver
import time
from library import locators
from selenium.webdriver.support import expected_conditions as EC


def current_driver():
    assert isinstance(config.DriverCache.current_driver, webdriver.Remote)
    return config.DriverCache.current_driver


def swipe_by_percent(start_x, start_y, end_x, end_y, duration=1000):
    width = current_driver().get_window_size()["width"]
    height = current_driver().get_window_size()["height"]
    x_start = float(start_x) / 100 * width
    x_end = float(end_x) / 100 * width
    y_start = float(start_y) / 100 * height
    y_end = float(end_y) / 100 * height
    x_offset = x_end - x_start
    y_offset = y_end - y_start
    platform = config.GlobalConfig.get_platform_name().lower()
    if platform == 'android':
        current_driver().swipe(x_start, y_start, x_end, y_end, duration)
    else:
        current_driver().swipe(x_start, y_start, x_offset, y_offset, duration)


class GuidePage(object):
    @staticmethod
    def jump_over_the_guide_page():
        print('[Begin Operation] Jump over guide pages', end='')
        current_driver().wait_activity("com.cmcc.cmrcs.android.ui.activities.SplashActivity", 3)
        swipe_by_percent(95, 50, 5, 50, 250)
        time.sleep(0.5)
        swipe_by_percent(95, 50, 5, 50, 250)
        EC.visibility_of_element_located(locators.p_welcome_m_main_e_start_to_use)
        ElementFinder.find_element(locators.p_welcome_m_main_e_start_to_use).click()
        print('[Operation Finish]')

    @staticmethod
    def click_start_to_use():
        ElementFinder.find_element(locators.p_welcome_m_main_e_start_to_use).click()


class PermissionListPage(object):
    @staticmethod
    def accept_all_permission_in_list():
        print('[Begin Operation] Accept all permissions in list', end='')
        EC.element_to_be_clickable(locators.p_permission_list_m_list_e_submit)
        ElementFinder.find_element(locators.p_permission_list_m_list_e_submit).click()
        print('[Operation Finish]')


class PermissionGrantPage(object):
    @staticmethod
    def get_total_number_of_permissions_and_now_index_from_dialog_footer():
        print('[Begin Operation] Get the number of permission dialog', end='')
        EC.presence_of_element_located(locators.p_permission_grant_m_dialog_e_dialog_box)
        footer = ElementFinder.find_element(locators.p_permission_grant_m_dialog_e_dialog_footer)
        now, count = re.findall('\d+', footer.text)
        print('[Operation Finish]')
        return int(now), int(count)

    @staticmethod
    def always_allow_popup_permission():
        print('[Begin Operation] Accept all', end='')
        now, count = list(PermissionGrantPage.get_total_number_of_permissions_and_now_index_from_dialog_footer())
        while now < count:
            now, count = PermissionGrantPage.get_total_number_of_permissions_and_now_index_from_dialog_footer()
            EC.element_to_be_clickable(locators.p_permission_grant_m_dialog_e_allow)
            ElementFinder.find_element(locators.p_permission_grant_m_dialog_e_allow).click()
            EC.invisibility_of_element(locators.p_permission_grant_m_dialog_e_dialog_box)

        print('[Operation Finish]')


class Login(object):
    @staticmethod
    def login_with_one_key_login():
        WebDriverWait(current_driver(), 3).until(EC.element_to_be_clickable(locators.p_login_m_one_key_e_one_key_login))
        ElementFinder.find_element(locators.p_login_m_one_key_e_phone_number).click()


class System(object):
    @staticmethod
    def click_ok_if_popup_permission_dialog():
        try:
            EC.element_to_be_clickable((MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("取消")'))
            ElementFinder.find_element((MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("取消")')).click()
        except:
            pass
