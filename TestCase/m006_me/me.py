import unittest
import uuid

from library.core.TestCase import TestCase
from library.core.utils import email_helper
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
import preconditions
from pages.components.PickGroup import PickGroupPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class MeTest(TestCase):
    """
    模块：我

    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：我
    """

    def setUp_test_me_0001(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @unittest.skip('该模块用例步骤描述有问题')
    def test_me_0001(self):
        """"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        qr_code.click_forward_qr_code()
        current_mobile().click_text("选择一个群", True)

        pg = PickGroupPage()
        pg.wait_for_page_load()
        pg.select_group('群聊1')
        current_mobile().click_text("确定", True)


class MeMsgSettingTest(TestCase):
    """
    模块：我-消息设置

    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：我-消息设置
    """

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_msg_setting_0001(self):
        """接收139邮箱助手信息默认开启"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.assert_menu_item_has_been_turn_on('接收139邮箱助手消息')

    @staticmethod
    def setUp_test_me_msg_setting_0001():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_msg_setting_0002(self):
        """开启接收139邮箱助手信息"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_on('接收139邮箱助手消息')
        msg_setting.assert_menu_item_has_been_turn_on('接收139邮箱助手消息')
        msg_setting.click_back()

        SettingPage().click_back()
        MePage().wait_for_page_load()
        MePage().open_message_page()

        msg_page = MessagePage()
        to_address = self.login_number + '@139.com'
        email_subject, body = email_helper.send_email(to_address, '工作日报终稿', '更新内容！')
        msg_page.assert_first_message_title_in_list_is('139邮箱助手', 60)
        msg_page.click_message('139邮箱助手')

        assistant_page = EmailAssistantPage()
        assistant_page.assert_the_first_message_is('19876283465', 30)
        assistant_page.click_message('19876283465')

        email_list = EmailListPage()
        email_list.assert_the_newest_email_is(email_subject, 30)

    def setUp_test_me_msg_setting_0002(self):
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        self.login_number = preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_msg_setting_0003(self):
        """关闭接收139邮箱助手信息"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_off('接收139邮箱助手消息')
        msg_setting.assert_menu_item_has_been_turn_off('接收139邮箱助手消息')
        msg_setting.click_back()

        SettingPage().click_back()
        MePage().open_message_page()

        msg_page = MessagePage()
        to_address = self.login_number + '@139.com'
        email_helper.send_email(to_address, '工作日报终稿', '更新内容！')
        msg_page.assert_139_message_not_appear(30)

    def setUp_test_me_msg_setting_0003(self):
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        self.login_number = preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_msg_setting_0004(self):
        """接收OA消息默认开启"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0004():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags('ALL', 'SMOKE', "CMCC")
    def test_me_msg_setting_0005(self):
        """开启接收OA消息(只验证开关，不验证消息接收)"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.turn_on('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0005():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_off('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_off('接收OA消息')

    @tags('ALL', 'SMOKE', "CMCC")
    def test_me_msg_setting_0006(self):
        """关闭接收OA消息(只验证开关，不验证消息接收)"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.turn_off('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_off('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0006():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_on('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')


class MeSmsSettingTest(TestCase):
    """
    模块：我-短信设置

    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：我-短信设置
    """

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_sms_setting_0001(self):
        """短信设置默认关闭状态"""
        sms_setting = SmsSettingPage()
        sms_setting.assert_menu_item_has_been_turn_off('应用内收发短信')

    @staticmethod
    def setUp_test_me_sms_setting_0001():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("短信设置")

    @tags('ALL', 'SMOKE', "移动+XX")
    def test_me_sms_setting_0002(self):
        """开启应用内收发短信"""
        sms_setting = SmsSettingPage()
        sms_setting.turn_on('应用内收发短信')
        sms_setting.click_button('我知道了')
        sms_setting.assert_menu_item_has_been_turn_on('应用内收发短信')
        sms_setting.click_back()

        SettingPage().click_back()
        MePage().open_message_page()

        # 切到另一台手机发短信，一定要确保配置的卡顺序与实际手机卡槽位置一致
        mobile2 = preconditions.connect_mobile(REQUIRED_MOBILES['Android-XX'])
        content = uuid.uuid4().__str__()
        send_number, card_type = mobile2.send_sms(self.login_number, content)

        # 切回来继续操作
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        msg_page = MessagePage()
        msg_page.click_message(send_number, 15)

        chat_page = ChatWindowPage()
        if chat_page.is_tips_display():
            chat_page.directly_close_tips_alert()
        chat_page.assert_message_content_display(content)

    def setUp_test_me_sms_setting_0002(self):
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        self.login_number = preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("短信设置")


# from library.core.utils.testcasefilter import set_tags
# set_tags('SMOKE')
if __name__ == '__main__':
    pass
