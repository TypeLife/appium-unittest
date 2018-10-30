import re
import unittest

from library.core import Keywords
from library.core.TestCase import TestCase
from library.core.utils.WebDriverCache import DriverCache
from pages import *


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

    def test_login_C0003(self, phone_number='13510772034', login_time=60):
        """移动账号登录"""
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()

        MessagePage().wait_for_page_load(login_time)

    def test_login_C0004(self, phone_number='13510772034', login_time=60):
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


if __name__ == '__main__':
    unittest.main()
