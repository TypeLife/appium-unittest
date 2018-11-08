import unittest
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import MOBILE_DRIVER_CACHE, current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    "测试机": 'M960BDQN229CH',
    "辅助机": 'jlyuan'
}


class CommonActions(object):
    @staticmethod
    def from_guide_page_to_login_page():
        guid_page = GuidePage()
        guid_page.wait_for_page_load()
        guid_page.swipe_to_the_second_banner()
        guid_page.swipe_to_the_third_banner()
        guid_page.click_start_the_experience()

        permission_list = PermissionListPage()
        permission_list.wait_for_page_load(30)
        permission_list.click_submit_button()

        onkey_page = OneKeyLoginPage()
        onkey_page.wait_for_page_load(30)
        onkey_page.wait_for_tell_number_load()

    @staticmethod
    def login_first_time():
        onekey = OneKeyLoginPage()
        onekey.wait_for_tell_number_load()
        onekey.click_one_key_login()
        onekey.click_read_agreement_detail()
        agreement_page = AgreementDetailPage()
        agreement_page.click_agree_button()
        message_page = MessagePage()
        message_page.wait_for_page_load(30)


class Demo(TestCase):
    """多手机协同DEMO"""

    @tags('SMOKE', 'SIT', 'DEMO_DEBUG')
    def test_multi_mobile_demo(self):
        """两台手机协同完成测试用例"""
        current_mobile().reset_app()
        mp = MessagePage()
        mp.wait_for_page_load()
        self.assertEqual(True, True)

    def setUp_test_multi_mobile_demo(self):
        """测试机已登录"""
        # 登录测试机
        switch_to_mobile(REQUIRED_MOBILES['测试机'])
        current_mobile().connect_mobile()
        current_mobile().reset_app()
        CommonActions.from_guide_page_to_login_page()
        CommonActions.login_first_time()

        # 登录辅助机
        switch_to_mobile(REQUIRED_MOBILES['辅助机'])
        current_mobile().connect_mobile()
        current_mobile().reset_app()
        CommonActions.from_guide_page_to_login_page()
        CommonActions.login_first_time()

        # 当前手机切换回测试机
        switch_to_mobile(REQUIRED_MOBILES['测试机'])

    def tearDown_test_multi_mobile_demo(self):
        MOBILE_DRIVER_CACHE.close_all()


if __name__ == '__main__':
    unittest.main()
