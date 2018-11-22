import re
import time
import unittest

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def select_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
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
        message_page.wait_for_page_load(60)

    @staticmethod
    def make_already_in_message_page():
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动')
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_have_my_group():
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            return
        sog.click_back()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        if not names:
            raise AssertionError("No contacts, please add contacts in address book.")
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def enter_group_chat_page():
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group()
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "mygroup" + phone_number[-4:]
        return group_name


class MsgGroupChatTest(TestCase):
    """消息->群聊 模块"""

    @classmethod
    def setUpClass(cls):
        """进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page()

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    def test_msg_group_chat_0001(self):
        """在群聊聊天会话页面，发送一段字符数等于“0”的文本字符"""
        gcp = GroupChatPage()
        # 语音按钮检查
        gcp.page_should_contain_audio_btn()

    def test_msg_group_chat_0002(self):
        """在群聊聊天会话页面，发送一段字符数大于“0”的文本字符"""
        gcp = GroupChatPage()
        info = "Hello everyone!"
        gcp.input_message(info)
        gcp.page_should_contain_send_btn()
        gcp.send_message()
        gcp.page_should_contain_text(info)

    def test_msg_group_chat_0003(self):
        """在群聊聊天会话页面，发送一段字符数小于等于“5000”的文本字符"""
        gcp = GroupChatPage()
        info = "Hello everyone, Welcome to my group, I hope my group can bring you happy."
        gcp.input_message(info)
        gcp.page_should_contain_send_btn()
        gcp.send_message()
        gcp.page_should_contain_text(info)

    def test_msg_group_chat_0004(self):
        """在群聊聊天会话页面，发送一段字符数等于“5000”的文本字符"""
        gcp = GroupChatPage()
        info = "哈哈" * 2500
        gcp.input_message(info)
        gcp.page_should_contain_send_btn()
        gcp.send_message()

    def test_msg_group_chat_0006(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        flag = cpg.send_btn_is_enabled()
        # 不选择图片，发送按钮不可点击
        self.assertEquals(flag, False)
        # 回到聊天回话页面
        cpg.click_back()

    def test_msg_group_chat_0007(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 选择图片
        cpg.select_pic()
        # 发送按钮可点击
        self.assertTrue(cpg.send_btn_is_enabled())
        cpg.click_send()
