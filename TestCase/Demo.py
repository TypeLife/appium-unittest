import unittest

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    "测试机": 'single_mobile',
    "辅助机2": 'M960BDQN229CH',
}


class Preconditions(object):
    """
    分解前置条件
    """

    @staticmethod
    def select_single_cmcc_android_4g_client():
        """
        启动
        1、4G，安卓客户端
        2、移动卡
        :return:
        """
        client = switch_to_mobile(REQUIRED_MOBILES['测试机'])
        client.connect_mobile()

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

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
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def make_already_in_sms_login_page():
        """
        1、已经进入短信登录页
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
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.wait_for_page_load(30)
        permission_list.click_submit_button()
        page_name = one_key.wait_one_key_or_sms_login_page_load(30)
        if page_name == 'sms':
            return
        one_key.choose_another_way_to_login()
        SmsLoginPage().wait_for_page_load()

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
        message_page.wait_for_page_load(60)

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def app_start_for_the_first_time():
        """首次启动APP（使用重置APP代替）"""
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
    def background_app(seconds):
        """后台运行"""
        current_mobile().background_app(seconds)

    @staticmethod
    def diff_card_make_already_in_sms_login_page():
        """确保异网卡已在短信登录界面"""
        sms = SmsLoginPage()
        if sms.is_on_this_page():
            return
        current_mobile().reset_app()
        guide_page = GuidePage()
        guide_page.wait_until(
            lambda d: guide_page.is_text_present("解锁“免费通信”新攻略")
        )
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 确定
        PermissionListPage(). \
            wait_for_page_load(). \
            click_submit_button()
        SmsLoginPage().wait_for_page_load()

    @staticmethod
    def diff_card_enter_sms_login_page():
        """异网卡进入短信登录界面"""
        Preconditions.select_single_cmcc_android_4g_client()
        Preconditions.diff_card_make_already_in_sms_login_page()


@unittest.skip('这是一个用例DEMO')
class Demo(TestCase):
    """多手机协同DEMO"""

    def setUp_test_login_0008(self):
        """测试机登录客户端、辅助机打开到验证码登录页"""
        # A手机已经登录
        Preconditions.select_single_cmcc_android_4g_client()
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()
        one_key = OneKeyLoginPage().wait_for_tell_number_load(120)
        self.login_number = one_key.get_login_number()
        Preconditions.login_by_one_key_login()

        # B手机进入短信登录界面
        Preconditions.select_assisted_mobile2()
        current_mobile().reset_app()
        Preconditions.make_already_in_sms_login_page()

    @tags('DEMO')
    def test_login_0008(self):
        """下线提醒"""
        # 切换到辅助机2，并用测试机的号码登录
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        sms_page = SmsLoginPage()
        sms_page.wait_for_page_load(30)
        sms_page.input_phone_number(self.login_number)
        # sms_page.click_get_code()

        # 切换回测试机取验证码
        mobile1 = switch_to_mobile(REQUIRED_MOBILES['测试机'])
        with mobile1.listen_verification_code(120) as code:
            switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
            sms_page.click_get_code()
        # code = sms_page.listen_verification_code(60)

        # 切换到辅助机2
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        sms_page.input_verification_code(code)
        sms_page.click_login()
        OneKeyLoginPage().click_read_agreement_detail()
        AgreementDetailPage().click_agree_button()
        sms_page.click_i_know()

        message_page = MessagePage()
        message_page.wait_for_page_load(60)

        # 切换回测试机等待下线提示
        switch_to_mobile(REQUIRED_MOBILES['测试机'])
        message_page.wait_until(
            condition=lambda d: message_page.is_text_present('下线通知'),
            timeout=30
        )


if __name__ == '__main__':
    unittest.main()
