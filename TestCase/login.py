import re
import unittest

from library.core import Keywords
from library.core.TestCase import TestCase
from library.core.utils.WebDriverCache import DriverCache
from pages import *
import time
import re
from appium.webdriver.common.mobileby import MobileBy


class LoginTest(TestCase):
    """Login 模块"""

    @classmethod
    def setUpClass(cls):
        if DriverCache.current_driver is None:
            Keywords.Android.open_app()

    @classmethod
    def tearDownClass(cls):
        Keywords.Android.closed_current_driver()

    def default_setUp(self):
        """
        预置条件：
        1、双卡手机
        2、测试机能正常联网
        """
        # self.assertIn(Keywords.Android.get_network_state_code(), [2, 4, 6])  # 存在有网但是状态为0 的情况，不可以作为是否有网的条件
        guide_page = GuidePage()
        if guide_page.driver.current_activity == guide_page.ACTIVITY:
            guide_page.wait_for_page_load()
            if guide_page._is_text_present("解锁“免费通信”新攻略"):
                guide_page.swipe_to_the_second_banner()
                guide_page.swipe_to_the_third_banner()
                guide_page.click_start_the_experience()

                # 确定
                PermissionListPage(). \
                    wait_for_page_load(). \
                    click_submit_button()

                # 等待页面进入一键登录页
                OneKeyLoginPage().wait_for_page_load()

        elif OneKeyLoginPage().is_current_activity_match_this_page():
            pass
        else:
            Keywords.Android.launch_app()
            guide_page.wait_for_page_load()
            guide_page.swipe_to_the_second_banner()
            guide_page.swipe_to_the_third_banner()
            guide_page.click_start_the_experience()

            # 确定
            PermissionListPage(). \
                wait_for_page_load(). \
                click_submit_button()

            # 等待页面进入一键登录页
            OneKeyLoginPage().wait_for_page_load()

    def default_tearDown(self):
        pass

    #@unittest.skip("skip 移动账号登录")
    def test_login_C0003(self, phone_number='14775970982', login_time=60):
        """移动账号登录"""
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()
        MessagePage().wait_for_page_load(login_time)

    @unittest.skip("skip 测试条件是双卡")
    def test_login_C0004(self, phone_number='14775970982', login_time=60):
        """切换验证码登录"""
        onekey = OneKeyLoginPage()
        onekey.wait_for_page_load()
        onekey.choose_another_way_to_login()

        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.input_phone_number(phone_number)
        result = sms.get_verification_code(60)
        self.assertIn('【登录验证】尊敬的用户', result)
        code = re.findall(r'\d+', result)
        sms.input_verification_code(code)
        sms.click_login()
        sms.click_i_know()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_C0005(self):
        """
        预置条件：
        1、异网账号
        2、测试机能正常联网
        """
        self.assertIn(Keywords.Android.get_network_state_code(), [2, 4, 6])
        guide_page = GuidePage()
        if guide_page.driver.current_activity == guide_page.ACTIVITY:
            if guide_page._is_text_present("解锁“免费通信”新攻略"):
                guide_page.swipe_to_the_second_banner()
                guide_page.swipe_to_the_third_banner()
                guide_page.click_start_the_experience()

                # 确定
                PermissionListPage(). \
                    wait_for_page_load(). \
                    click_submit_button()
                SmsLoginPage().wait_for_page_load()

    @unittest.skip("skip 异网账户测试")
    def test_login_C0005(self, phone_number='18681151872', login_time=60):
        """异网账号登录"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        sl.click_get_code()
        time.sleep(30)
        driver = Keywords.current_driver()
        # 打开通知栏，通过通知栏获取验证码
        Keywords.Android.open_notifications()
        time.sleep(5)
        # 获取验证码
        el = driver.find_element(MobileBy.ID, "android:id/text")
        self.assertIsNotNone(el)
        code = re.findall('\d{3,8}', el.text)[0]
        # 通知栏回退
        Keywords.Android.back()
        # 输入验证码，点击登录
        sl.input_verification_code(code)
        sl.click_login()
        time.sleep(5)
        # 点击‘我知道了’
        sl.click_i_know()
        MessagePage().wait_for_page_load(login_time)


if __name__ == '__main__':
    unittest.main()
