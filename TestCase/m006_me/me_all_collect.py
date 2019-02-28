import time
import unittest
import uuid

from appium.webdriver.common.mobileby import MobileBy

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.me.MeEditUserProfile import MeEditUserProfilePage
from pages.me.MeViewUserProfile import MeViewUserProfilePage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
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
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
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
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
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
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail():
            one_key.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_me_all_page():
        """确保应用在消息页面"""

        # 如果在消息页，不做任何操作
        mess = MessagePage()
        mep = MePage()
        if mep.is_on_this_page():
            return
        if mess.is_on_this_page():
            mess.open_me_page()
            mep.is_on_this_page()
            return
        # 进入一键登录页
        Preconditions.make_already_in_message_page(reset=False)
        mess.open_me_page()

    @staticmethod
    def make_already_set_message():
        """确保已经发送一条消息"""
        Preconditions.make_already_in_message_page()
        # 1.点击新建消息
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        mess.click_new_message()
        # 2.选择联系人发送一条消息
        scp = SelectContactsPage()
        scp.wait_for_page_local_contact_load()
        scp.click_one_contact("大佬1")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            bcp.click_i_have_read()
        infor = "测试工程师"
        bcp.input_message(infor * 30)
        bcp.send_message()
        # 3.点击该信息收藏
        mess.press_file_to_do("测试工程师", "收藏")
        if not bcp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        bcp.click_element(["id", 'com.chinasofti.rcs:id/back_arrow'])


class MeAllCollect(TestCase):
    """_
    模块：我的

    文件位置：全量/4.我模块全量测试用例-张淑丽.xlsx
    表格：我页面（收藏模块406后）

    """

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @staticmethod
    def setUp_test_me_all_page_406():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_set_message()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_406(self):
        """我页面跳转验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("我", "我")

