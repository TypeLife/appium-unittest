import unittest

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
}


class Preconditions(object):
    """
    分解前置条件
    """

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(30)
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        if current_driver().current_package == app_package:
            current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()


@unittest.skip("模板")
class MeTest(TestCase):
    """Me 模块"""

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    def test_something(self):
        """description"""
        self.assertEqual(True, False)

    def setUp_test_something(self):
        print("Run test case setup.")


class MeMsgSettingTest(TestCase):
    """我-消息设置"""

    @tags("ALL", "SMOKE")
    def test_me_msg_setting_0001(self):
        """接收139邮箱助手信息默认开启"""
        msg_setting = SetMessageNoticePage()
        msg_setting.assert_menu_item_has_been_turn_on('接收139邮箱助手消息')

    @staticmethod
    def setUp_test_me_msg_setting_0001():
        Preconditions.connect_mobile('Android-移动')
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE")
    def test_me_msg_setting_0004(self):
        """接收OA消息默认开启"""
        msg_setting = SetMessageNoticePage()
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0004():
        Preconditions.connect_mobile('Android-移动')
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")


# from library.core.utils.testcasefilter import set_tags
# set_tags('SMOKE')
if __name__ == '__main__':
    pass
