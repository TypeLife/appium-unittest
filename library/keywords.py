import re
import time

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from library import config
from library import locators
from library.core.testlogger import TestLogger
from library.elementfinder import ElementFinder


def current_driver():
    # assert isinstance(config.DriverCache.current_driver, webdriver.Remote)
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


class Android(object):
    @staticmethod
    @TestLogger.log()
    def open_app(server_url, desired_caps, alis=None):
        """打开app"""
        config.DriverCache.open_app(server_url, desired_caps, alis)

    @staticmethod
    @TestLogger.log()
    def closed_current_driver():
        config.DriverCache.close_current()

    @staticmethod
    @TestLogger.log()
    def install_app(app_path, **options):
        current_driver().install_app(app_path, **options)

    @staticmethod
    @TestLogger.log()
    def open_notifications():
        current_driver().open_notifications()

    @staticmethod
    @TestLogger.log()
    def back():
        current_driver().back()

    @staticmethod
    @TestLogger.log()
    def wait_new_verification_code(before, timeout=120):
        WebDriverWait(current_driver(), timeout).until(
            lambda d: before != Android.get_last_verification_code())

    @staticmethod
    @TestLogger.log()
    def get_last_verification_code():
        message = ElementFinder.find_elements(locators.p_notification_m_message_e_verification_code)
        if message.__len__():
            code = re.findall(r'\d+', message[0].text)[0]
        else:
            code = None
        return code

    @staticmethod
    @TestLogger.log()
    def go_back_to_app():
        current_driver().activate_app(current_driver().desired_capabilities['appPackage'])

    @staticmethod
    @TestLogger.log()
    def execute_shell_command(command, *args):
        """
        Execute ADB shell commands (requires server flag --relaxed-security to be set)

        例：execute_shell_command('am', 'start', '-n', 'com.example.demo/com.example.test.MainActivity')

        :param command: 例：am,pm 等等可执行命令
        :param args: 例：am,pm 等可执行命令的参数
        :return:
        """
        script = {
            'command': command,
            'args': args
        }
        return current_driver().execute_script('mobile:shell', script)


class Common(object):
    @staticmethod
    @TestLogger.log()
    def wait_activity_leave_form(activity, timeout=10):
        WebDriverWait(current_driver(), timeout).until(lambda d: activity != current_driver().current_activity)

    @staticmethod
    @TestLogger.log()
    def allow_all_permissions_if_needed():
        def is_permission_alert_present(driver):
            try:
                alert = driver.switch_to.alert
                return alert.accept
            except NoAlertPresentException:
                alert = ElementFinder.find_elements(
                    (MobileBy.XPATH, '//*[@text="始终允许"]')) or ElementFinder.find_elements(
                    (MobileBy.XPATH, '//*[@text="允许"]'))
                if not alert:
                    return False
                return alert[0].click

        if current_driver().current_activity == 'com.android.packageinstaller.permission.ui.GrantPermissionsActivity':
            need = True
            while need:
                try:
                    WebDriverWait(current_driver(), 1).until(
                        # EC.alert_is_present()
                        is_permission_alert_present
                    )()
                    # current_driver().switch_to.alert.accept()
                except:
                    need = False

    # ================================对话框确定按钮========================
    @staticmethod
    @TestLogger.log()
    def click_ok():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_all_page_m_dialog_e_ok)
        )
        ElementFinder.find_element(locators.p_all_page_m_dialog_e_ok).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_ok_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_all_page_m_dialog_e_ok).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_ok_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_all_page_m_dialog_e_ok).text
        )

    @staticmethod
    @TestLogger.log()
    def ok_should_clickable():
        EC.element_to_be_clickable(locators.p_all_page_m_dialog_e_ok)

    @staticmethod
    @TestLogger.log()
    def ok_text_should_be(text):
        assert ElementFinder.find_element(locators.p_all_page_m_dialog_e_ok).text == text
    # ===========================================================================


class GuidePage(object):

    @staticmethod
    @TestLogger.log()
    def jump_over_the_guide_page():
        """跳过引导页"""
        current_driver().wait_activity("com.cmcc.cmrcs.android.ui.activities.SplashActivity", 3)
        swipe_by_percent(95, 50, 5, 50, 250)
        time.sleep(0.5)
        swipe_by_percent(95, 50, 5, 50, 250)
        WebDriverWait(current_driver(), 20).until(EC.element_to_be_clickable(locators.p_welcome_m_main_e_start_to_use))
        ElementFinder.find_element(locators.p_welcome_m_main_e_start_to_use).click()

    @staticmethod
    @TestLogger.log()
    def click_start_to_use():
        ElementFinder.find_element(locators.p_welcome_m_main_e_start_to_use).click()


class PermissionListPage(object):
    @staticmethod
    @TestLogger.log()
    def accept_all_permission_in_list():
        EC.element_to_be_clickable(locators.p_permission_list_m_list_e_submit)
        current_activity = current_driver().current_activity
        ElementFinder.find_element(locators.p_permission_list_m_list_e_submit).click()
        Common.wait_activity_leave_form(current_activity)
        Common.allow_all_permissions_if_needed()


class PermissionGrantPage(object):
    @staticmethod
    @TestLogger.log()
    def get_total_number_of_permissions_and_now_index_from_dialog_footer():
        EC.presence_of_element_located(locators.p_permission_grant_m_dialog_e_dialog_box)
        footer = ElementFinder.find_element(locators.p_permission_grant_m_dialog_e_dialog_footer)
        now, count = re.findall('\d+', footer.text)
        return int(now), int(count)

    @staticmethod
    @TestLogger.log()
    def always_allow_popup_permission():
        # now, count = list(PermissionGrantPage.get_total_number_of_permissions_and_now_index_from_dialog_footer())
        # while now < count:
        skip = False
        while not skip:
            try:
                WebDriverWait(current_driver(), 1).until(EC.alert_is_present())
                current_driver().switch_to.alert.accept()
            except:
                skip = True
            # now, count = PermissionGrantPage.get_total_number_of_permissions_and_now_index_from_dialog_footer()
            # ElementFinder.find_element(locators.p_permission_grant_m_dialog_e_allow).click()


class MessagePage(object):

    # ================================右上角加号========================
    @staticmethod
    @TestLogger.log()
    def click_add_button():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_top_e_add_button)
        )
        ElementFinder.find_element(locators.p_message_m_top_e_add_button).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_add_button_clickable(timeout=10):
        WebDriverWait(current_driver(), timeout).until(
            EC.element_to_be_clickable(locators.p_message_m_top_e_add_button)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_add_button_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_message_m_top_e_add_button).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_add_button_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_message_m_top_e_add_button).text
        )

    @staticmethod
    @TestLogger.log()
    def add_button_should_clickable():
        EC.element_to_be_clickable(locators.p_message_m_top_e_add_button)

    @staticmethod
    @TestLogger.log()
    def add_button_text_should_be(text):
        assert ElementFinder.find_element(locators.p_message_m_top_e_add_button).text == text

    # ==================================================================

    # ================================新建消息========================
    @staticmethod
    @TestLogger.log()
    def click_new_message():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_new_message)
        )
        ElementFinder.find_element(locators.p_message_m_add_menu_e_new_message).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_new_message_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_new_message)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_new_message_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_message_m_add_menu_e_new_message).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_new_message_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_message_m_add_menu_e_new_message).text
        )

    @staticmethod
    @TestLogger.log()
    def new_message_should_clickable():
        EC.element_to_be_clickable(locators.p_message_m_add_menu_e_new_message)

    @staticmethod
    @TestLogger.log()
    def new_message_text_should_be(text):
        assert ElementFinder.find_element(locators.p_message_m_add_menu_e_new_message).text == text

    # ==================================================================

    # ================================免费短信========================
    @staticmethod
    @TestLogger.log()
    def click_free_sms():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_free_sms)
        )
        ElementFinder.find_element(locators.p_message_m_add_menu_e_free_sms).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_free_sms_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_free_sms)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_free_sms_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_message_m_add_menu_e_free_sms).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_free_sms_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_message_m_add_menu_e_free_sms).text
        )

    @staticmethod
    @TestLogger.log()
    def free_sms_should_clickable():
        EC.element_to_be_clickable(locators.p_message_m_add_menu_e_free_sms)

    @staticmethod
    @TestLogger.log()
    def free_sms_text_should_be(text):
        assert ElementFinder.find_element(locators.p_message_m_add_menu_e_free_sms).text == text

    # ==================================================================

    # ================================发起群聊========================
    @staticmethod
    @TestLogger.log()
    def click_initiate_group_chat():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_initiate_group_chat)
        )
        ElementFinder.find_element(locators.p_message_m_add_menu_e_initiate_group_chat).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_initiate_group_chat_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_initiate_group_chat)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_initiate_group_chat_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_message_m_add_menu_e_initiate_group_chat).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_initiate_group_chat_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_message_m_add_menu_e_initiate_group_chat).text
        )

    @staticmethod
    @TestLogger.log()
    def initiate_group_chat_should_clickable():
        EC.element_to_be_clickable(locators.p_message_m_add_menu_e_initiate_group_chat)

    @staticmethod
    @TestLogger.log()
    def initiate_group_chat_text_should_be(text):
        assert ElementFinder.find_element(locators.p_message_m_add_menu_e_initiate_group_chat).text == text

    # ==================================================================

    # ================================分组群发========================
    @staticmethod
    @TestLogger.log()
    def click_grouping_mass_message():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_grouping_mass_message)
        )
        ElementFinder.find_element(locators.p_message_m_add_menu_e_grouping_mass_message).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_grouping_mass_message_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_grouping_mass_message)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_grouping_mass_message_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_message_m_add_menu_e_grouping_mass_message).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_grouping_mass_message_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_message_m_add_menu_e_grouping_mass_message).text
        )

    @staticmethod
    @TestLogger.log()
    def grouping_mass_message_should_clickable():
        EC.element_to_be_clickable(locators.p_message_m_add_menu_e_grouping_mass_message)

    @staticmethod
    @TestLogger.log()
    def grouping_mass_message_text_should_be(text):
        assert ElementFinder.find_element(locators.p_message_m_add_menu_e_grouping_mass_message).text == text

    # ==================================================================

    # ================================扫一扫========================
    @staticmethod
    @TestLogger.log()
    def click_take_a_scan():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_take_a_scan)
        )
        ElementFinder.find_element(locators.p_message_m_add_menu_e_take_a_scan).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_take_a_scan_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_message_m_add_menu_e_take_a_scan)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_take_a_scan_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_message_m_add_menu_e_take_a_scan).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_take_a_scan_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_message_m_add_menu_e_take_a_scan).text
        )

    @staticmethod
    @TestLogger.log()
    def take_a_scan_should_clickable():
        EC.element_to_be_clickable(locators.p_message_m_add_menu_e_take_a_scan)

    @staticmethod
    @TestLogger.log()
    def take_a_scan_text_should_be(text):
        assert ElementFinder.find_element(locators.p_message_m_add_menu_e_take_a_scan).text == text

    # ==================================================================

    @staticmethod
    @TestLogger.log()
    def wait_for_message_page_load(timeout=8):
        current_driver().wait_activity('com.cmcc.cmrcs.android.ui.activities.HomeActivity', timeout)
        MessagePage.wait_for_add_button_clickable()


class SelectContactPage(object):
    @staticmethod
    @TestLogger.log()
    def wait_for_select_contact_page_load(timeout=5):
        WebDriverWait(current_driver(), timeout).until(
            lambda d: current_driver().current_activity == 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'
        )
        SelectContactPage.wait_for_contact_search_box_clickable()

    @staticmethod
    @TestLogger.log()
    def select_contact_by_given_index(index):
        """
        选择第n联系人
        :param index: 从1开始算
        :return:
        """
        locator = list(locators.SelectContactPage.p_select_contact_m_contact_list_e_contact)
        locator[1] = locator[1] + '.index({})'.format(index - 1)
        WebDriverWait(current_driver(), 5).until(
            EC.element_to_be_clickable(locator)
        )
        ElementFinder.find_element(locator).click()

    @staticmethod
    @TestLogger.log()
    def get_concat_name_by_given_index(index):
        parent = list(locators.SelectContactPage.p_select_contact_m_contact_list_e_contact)
        parent[1] = parent[1] + '.index({})'.format(index - 1)
        locator = [parent[0], parent[1] + '.childSelector({})'.format(
            locators.SelectContactPage.p_select_contact_m_contact_list_e_contact_name[1])]
        return ElementFinder.find_element(locator).text

    @staticmethod
    @TestLogger.log()
    def get_concat_number_by_given_index(index):
        parent = list(locators.SelectContactPage.p_select_contact_m_contact_list_e_contact)
        parent[1] = parent[1] + '.index({})'.format(index - 1)
        locator = [parent[0], parent[1] + '.childSelector({})'.format(
            locators.SelectContactPage.p_select_contact_m_contact_list_e_contact_number[1])]
        return ElementFinder.find_element(locator).text

    # ===========================联系人搜索框=============================
    @staticmethod
    @TestLogger.log()
    def input_contact_search_box(text):
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.SelectContactPage.p_select_contact_m_search_e_search_box)
        )
        ElementFinder.find_element(locators.SelectContactPage.p_select_contact_m_search_e_search_box).send_keys(text)

    @staticmethod
    @TestLogger.log()
    def wait_for_contact_search_box_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.SelectContactPage.p_select_contact_m_search_e_search_box)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_contact_search_box_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(
                locators.SelectContactPage.p_select_contact_m_search_e_search_box).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_contact_search_box_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(
                locators.SelectContactPage.p_select_contact_m_search_e_search_box).text
        )

    @staticmethod
    @TestLogger.log()
    def contact_search_box_should_clickable():
        EC.element_to_be_clickable(locators.SelectContactPage.p_select_contact_m_search_e_search_box)

    @staticmethod
    @TestLogger.log()
    def contact_search_box_text_should_be(text):
        assert ElementFinder.find_element(
            locators.SelectContactPage.p_select_contact_m_search_e_search_box).text == text

    # ==================================================================


class MessageDetailPage(object):
    @staticmethod
    @TestLogger.log()
    def wait_for_message_detail_page_load(timeout=8):
        WebDriverWait(current_driver(), timeout).until(
            lambda d: current_driver().current_activity == 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity')

    @staticmethod
    @TestLogger.log()
    def wait_for_user_remind_popup(timeout=5):
        WebDriverWait(current_driver(), timeout).until(
            lambda d: '用户须知' in current_driver().page_source
        )

    @staticmethod
    @TestLogger.log()
    def accept_remind_dialog_and_close_it():
        # 勾选我已阅读
        WebDriverWait(current_driver(), 5).until(
            EC.visibility_of_element_located(locators.MessageDetailPage.p_message_detail_m_dialog_e_is_read))
        if not ElementFinder.find_element(locators.MessageDetailPage.p_message_detail_m_dialog_e_is_read).is_selected():
            ElementFinder.find_element(locators.MessageDetailPage.p_message_detail_m_dialog_e_is_read).click()

        # 点击确定
        WebDriverWait(current_driver(), 1).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_dialog_e_ok_button)
        )
        ElementFinder.find_element(locators.MessageDetailPage.p_message_detail_m_dialog_e_ok_button).click()
        # 等待对话框消失
        WebDriverWait(current_driver(), 2).until(
            lambda d: '用户须知' not in current_driver().page_source
        )

    @staticmethod
    @TestLogger.log()
    def remind_dialog_should_not_display():
        if ElementFinder.find_elements(locators.MessageDetailPage.p_message_detail_m_dialog_e_is_read):
            print(current_driver().page_source)
            raise AssertionError("用户须知对话框不应该显示")

    # ==========================消息输入框==============================
    @staticmethod
    @TestLogger.log()
    def input_text_to_message_input_box(text):
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_m_bottom_e_message_input_box)
        )
        ElementFinder.find_element(locators.MessageDetailPage.p_message_m_bottom_e_message_input_box).send_keys(text)

    @staticmethod
    @TestLogger.log()
    def wait_for_message_input_box_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_m_bottom_e_message_input_box)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_message_input_box_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(
                locators.MessageDetailPage.p_message_m_bottom_e_message_input_box).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_message_input_box_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(
                locators.MessageDetailPage.p_message_m_bottom_e_message_input_box).text
        )

    @staticmethod
    @TestLogger.log()
    def message_input_box_should_clickable():
        EC.element_to_be_clickable(locators.MessageDetailPage.p_message_m_bottom_e_message_input_box)

    @staticmethod
    @TestLogger.log()
    def message_input_box_text_should_be(text):
        assert ElementFinder.find_element(
            locators.MessageDetailPage.p_message_m_bottom_e_message_input_box).text == text

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    @TestLogger.log()
    def input_message_and_send(message):
        MessageDetailPage.input_text_to_message_input_box(message)
        MessageDetailPage.click_send_message_button()

    # ================================发送消息按钮========================
    @staticmethod
    @TestLogger.log()
    def click_send_message_button():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button)
        )
        ElementFinder.find_element(locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_send_message_button_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_send_message_button_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(
                locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_send_message_button_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(
                locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button).text
        )

    @staticmethod
    @TestLogger.log()
    def send_message_button_should_clickable():
        EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button)

    @staticmethod
    @TestLogger.log()
    def send_message_button_text_should_be(text):
        assert ElementFinder.find_element(
            locators.MessageDetailPage.p_message_detail_m_bottom_e_send_message_button).text == text

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # =========================消息顶部标题===============================
    @staticmethod
    @TestLogger.log()
    def click_title():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_title_e_title)
        )
        ElementFinder.find_element(locators.MessageDetailPage.p_message_detail_m_title_e_title).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_title_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_title_e_title)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_title_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(
                locators.MessageDetailPage.p_message_detail_m_title_e_title).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_title_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(
                locators.MessageDetailPage.p_message_detail_m_title_e_title).text
        )

    @staticmethod
    @TestLogger.log()
    def title_should_clickable():
        EC.element_to_be_clickable(locators.MessageDetailPage.p_message_detail_m_title_e_title)

    @staticmethod
    @TestLogger.log()
    def title_text_should_be(text):
        assert ElementFinder.find_element(locators.MessageDetailPage.p_message_detail_m_title_e_title).text == text

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # =========================消息顶部标题===============================
    @staticmethod
    @TestLogger.log()
    def click_last_message():
        message_blocks = ElementFinder.find_elements(
            locators.MessageDetailPage.p_message_detail_m_message_list_e_message_block)
        if not message_blocks:
            raise NoSuchElementException("消息列表是空的")
        message_text = message_blocks[-1].find_element(
            locators.MessageDetailPage.p_message_detail_m_message_list_e_message)
        message_text.click()

    @staticmethod
    @TestLogger.log()
    def get_last_message_text():
        message_blocks = ElementFinder.find_elements(
            locators.MessageDetailPage.p_message_detail_m_message_list_e_message_block)
        if not message_blocks:
            raise NoSuchElementException("消息列表是空的")
        message_text = message_blocks[-1].find_element(
            locators.MessageDetailPage.p_message_detail_m_message_list_e_message)
        return message_text.text

    @staticmethod
    @TestLogger.log()
    def is_last_message_has_send_ok_state():
        message_blocks = ElementFinder.find_elements(
            locators.MessageDetailPage.p_message_detail_m_message_list_e_message_block)
        if not message_blocks:
            raise NoSuchElementException("消息列表是空的")
        send_ok = message_blocks[-1].find_elements(
            locators.MessageDetailPage.p_message_detail_m_message_list_e_send_ok_state)
        return send_ok.text

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class HomePageFooter(object):
    @staticmethod
    @TestLogger.log()
    def open_page_me_by_click_me():
        WebDriverWait(current_driver(), 3).until(EC.element_to_be_clickable(locators.p_home_m_footer_e_me))
        ElementFinder.find_element(locators.p_home_m_footer_e_me).click()


class MePage(object):
    @staticmethod
    @TestLogger.log()
    def click_setting():
        # me = ElementFinder.find_element(locators.p_home_m_footer_e_me)
        # current_driver().execute_script("mobile: shell", {"direction": 'up', 'element': me.id})
        WebDriverWait(current_driver(), 3).until(EC.element_to_be_clickable(locators.p_home_m_me_e_setting))
        ElementFinder.find_element(locators.p_home_m_me_e_setting).click()


class SettingHomePage(object):
    @staticmethod
    @TestLogger.log()
    def logout_app_by_click_quit():
        WebDriverWait(current_driver(), 3).until(EC.element_to_be_clickable(locators.p_home_m_setting_home_e_quit))
        ElementFinder.find_element(locators.p_home_m_setting_home_e_quit).click()
        Common.click_ok()


class Login(object):
    @staticmethod
    @TestLogger.log()
    def wait_for_one_key_login_page_load():
        # 检查界面是否加载11位电话号码
        WebDriverWait(current_driver(), 8).until(lambda d: re.fullmatch('\d{11}', ElementFinder.find_element(
            locators.p_login_m_one_key_e_phone_number).text))

    # ================================对话框确定按钮========================
    @staticmethod
    @TestLogger.log()
    def click_one_key_login():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_login_m_one_key_e_one_key_login)
        )
        current_activity = current_driver().current_activity
        ElementFinder.find_element(locators.p_login_m_one_key_e_one_key_login).click()

        # 等待登录中出现并消失
        WebDriverWait(current_driver(), 15).until(
            lambda d: '正在登录' in current_driver().page_source
        )
        WebDriverWait(current_driver(), 60).until(
            lambda d: '正在登录' not in current_driver().page_source
        )
        Common.wait_activity_leave_form(current_activity)
        Common.allow_all_permissions_if_needed()

    @staticmethod
    @TestLogger.log()
    def wait_for_one_key_login_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_login_m_one_key_e_one_key_login).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_one_key_login_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_login_m_one_key_e_one_key_login).text
        )

    @staticmethod
    @TestLogger.log()
    def one_key_login_should_clickable():
        EC.element_to_be_clickable(locators.p_login_m_one_key_e_one_key_login)

    @staticmethod
    @TestLogger.log()
    def one_key_login_text_should_be(text):
        assert ElementFinder.find_element(locators.p_login_m_one_key_e_one_key_login).text == text

    # ==================================================================

    @staticmethod
    @TestLogger.log()
    def login_with_one_key_login():
        WebDriverWait(current_driver(), 3).until(EC.element_to_be_clickable(locators.p_login_m_one_key_e_one_key_login))
        ElementFinder.find_element(locators.p_login_m_one_key_e_phone_number).click()

    # ================等待activity加载=====================
    @staticmethod
    @TestLogger.log()
    def wait_for_sms_login_page_load():
        current_driver().wait_activity('com.cmcc.cmrcs.android.ui.activities.SmsLoginActivity', 3)

    # =====================================

    # ================================切换另一号码登录========================
    @staticmethod
    @TestLogger.log()
    def click_use_another_number_to_login():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_login_m_form_e_use_another_number_to_login)
        )
        ElementFinder.find_element(locators.p_login_m_form_e_use_another_number_to_login).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_use_another_number_to_login_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_login_m_form_e_use_another_number_to_login).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_use_another_number_to_login_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_login_m_form_e_use_another_number_to_login).text
        )

    @staticmethod
    @TestLogger.log()
    def use_another_number_to_login_should_clickable():
        EC.element_to_be_clickable(locators.p_login_m_form_e_use_another_number_to_login)

    @staticmethod
    @TestLogger.log()
    def use_another_number_to_login_text_should_be(text):
        assert ElementFinder.find_element(locators.p_login_m_form_e_use_another_number_to_login).text == text

    # ==================================================================

    # ================================手机号码输入框========================
    @staticmethod
    @TestLogger.log()
    def input_phone_number(phone_number):
        WebDriverWait(current_driver(), 3).until(
            EC.visibility_of_element_located(locators.p_sms_login_m_form_e_phone_number)
        )
        ElementFinder.find_element(locators.p_sms_login_m_form_e_phone_number).send_keys(phone_number)
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_sms_login_m_form_e_phone_number).text == phone_number
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_phone_number_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_sms_login_m_form_e_phone_number).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_phone_number_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_sms_login_m_form_e_phone_number).text
        )

    @staticmethod
    @TestLogger.log()
    def phone_number_should_clickable():
        EC.element_to_be_clickable(locators.p_sms_login_m_form_e_phone_number)

    @staticmethod
    @TestLogger.log()
    def phone_number_text_should_be(text):
        assert ElementFinder.find_element(locators.p_sms_login_m_form_e_phone_number).text == text

    # ==================================================================

    # ================================获取验证码========================
    @staticmethod
    @TestLogger.log()
    def click_get_verification_code():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_sms_login_m_form_e_get_verification_code)
        )
        ElementFinder.find_element(locators.p_sms_login_m_form_e_get_verification_code).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_get_verification_code_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_sms_login_m_form_e_get_verification_code)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_get_verification_code_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_sms_login_m_form_e_get_verification_code).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_get_verification_code_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_sms_login_m_form_e_get_verification_code).text
        )

    @staticmethod
    @TestLogger.log()
    def get_verification_code_should_clickable():
        EC.element_to_be_clickable(locators.p_sms_login_m_form_e_get_verification_code)

    @staticmethod
    @TestLogger.log()
    def get_verification_code_text_should_be(text):
        assert ElementFinder.find_element(locators.p_sms_login_m_form_e_get_verification_code).text == text

    # ==================================================================

    # ================================验证码输入框========================
    @staticmethod
    @TestLogger.log()
    def input_verification_code(code):
        WebDriverWait(current_driver(), 3).until(
            EC.visibility_of_element_located(locators.p_sms_login_m_form_e_verification_code)
        )
        ElementFinder.find_element(locators.p_sms_login_m_form_e_verification_code).send_keys(code)

    @staticmethod
    @TestLogger.log()
    def wait_for_verification_code_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_sms_login_m_form_e_verification_code).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_verification_code_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_sms_login_m_form_e_verification_code).text
        )

    @staticmethod
    @TestLogger.log()
    def verification_code_should_clickable():
        EC.element_to_be_clickable(locators.p_sms_login_m_form_e_verification_code)

    @staticmethod
    @TestLogger.log()
    def verification_code_text_should_be(text):
        assert ElementFinder.find_element(locators.p_sms_login_m_form_e_verification_code).text == text

    # ==================================================================

    # ================================对话框确定按钮========================
    @staticmethod
    @TestLogger.log()
    def click_login():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_sms_login_m_form_e_login)
        )
        ElementFinder.find_element(locators.p_sms_login_m_form_e_login).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_login_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_sms_login_m_form_e_login).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_login_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_sms_login_m_form_e_login).text
        )

    @staticmethod
    @TestLogger.log()
    def login_should_clickable():
        EC.element_to_be_clickable(locators.p_sms_login_m_form_e_login)

    @staticmethod
    @TestLogger.log()
    def login_text_should_be(text):
        assert ElementFinder.find_element(locators.p_sms_login_m_form_e_login).text == text

    # ==================================================================

    # ================================对话框确定按钮========================
    @staticmethod
    @TestLogger.log()
    def click_i_know():
        WebDriverWait(current_driver(), 15).until(
            EC.element_to_be_clickable(locators.p_sms_login_m_dialog_e_i_know)
        )
        current_activity = current_driver().current_activity
        ElementFinder.find_element(locators.p_sms_login_m_dialog_e_i_know).click()

        WebDriverWait(current_driver(), 15).until(lambda d: '正在登录' in current_driver().page_source)
        WebDriverWait(current_driver(), 60).until(lambda d: '正在登录' not in current_driver().page_source)
        Common.wait_activity_leave_form(current_activity)
        Common.allow_all_permissions_if_needed()

    @staticmethod
    @TestLogger.log()
    def wait_for_i_know_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_sms_login_m_dialog_e_i_know).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_i_know_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_sms_login_m_dialog_e_i_know).text
        )

    @staticmethod
    @TestLogger.log()
    def i_know_should_clickable():
        EC.element_to_be_clickable(locators.p_sms_login_m_dialog_e_i_know)

    @staticmethod
    @TestLogger.log()
    def i_know_text_should_be(text):
        assert ElementFinder.find_element(locators.p_sms_login_m_dialog_e_i_know).text == text

    # ==================================================================


class System(object):
    @staticmethod
    @TestLogger.log()
    def click_ok_if_popup_permission_dialog():
        try:
            EC.element_to_be_clickable((MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("取消")'))
            ElementFinder.find_element((MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("取消")')).click()
        except:
            pass


class Demo(object):

    # ========================================================
    @staticmethod
    @TestLogger.log()
    def click_element():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_demo_m_module_e_element)
        )
        ElementFinder.find_element(locators.p_demo_m_module_e_element).click()

    @staticmethod
    @TestLogger.log()
    def wait_for_element_clickable():
        WebDriverWait(current_driver(), 3).until(
            EC.element_to_be_clickable(locators.p_demo_m_module_e_element)
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_element_text_match(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: ElementFinder.find_element(locators.p_demo_m_module_e_element).text == text
        )

    @staticmethod
    @TestLogger.log()
    def wait_for_element_text_contain(text):
        WebDriverWait(current_driver(), 3).until(
            lambda d: text in ElementFinder.find_element(locators.p_demo_m_module_e_element).text
        )

    @staticmethod
    @TestLogger.log()
    def element_should_clickable():
        EC.element_to_be_clickable(locators.p_demo_m_module_e_element)

    @staticmethod
    @TestLogger.log()
    def element_text_should_be(text):
        assert ElementFinder.find_element(locators.p_demo_m_module_e_element).text == text

    # ==================================================================

# class LiveTemplate(object):
#     p_$PageName$_m_$ModuleName$_e_$ElementName$ = ($By$, '$Locator$')
#
#     @staticmethod
#     def click_$ElementName$():
#         WebDriverWait(current_driver(), 3).until(
#             EC.element_to_be_clickable(locators.p_$PageName$_m_$ModuleName$_e_$ElementName$)
#         )
#         ElementFinder.find_element(locators.p_$PageName$_m_$ModuleName$_e_$ElementName$).click()
#
#     @staticmethod
#     def wait_for_$ElementName$_text_match(text):
#         WebDriverWait(current_driver(), 3).until(
#             lambda d: ElementFinder.find_element(locators.p_$PageName$_m_$ModuleName$_e_$ElementName$).text == text
#         )
#
#     @staticmethod
#     def wait_for_$ElementName$_text_containt(text):
#         WebDriverWait(current_driver(), 3).until(
#             lambda d: text in ElementFinder.find_element(locators.p_$PageName$_m_$ModuleName$_e_$ElementName$).text
#         )
#
#     @staticmethod
#     def $ElementName$_should_clickable():
#         EC.element_to_be_clickable(locators.p_$PageName$_m_$ModuleName$_e_$ElementName$)
#
#     @staticmethod
#     def $ElementName$_text_should_be(text):
#         assert ElementFinder.find_element(locators.p_$PageName$_m_$ModuleName$_e_$ElementName$).text == text
