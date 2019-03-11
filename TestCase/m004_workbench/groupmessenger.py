import unittest

import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import switch_to_mobile, current_mobile
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage
from pages import GuidePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.group_messenger.MessageGroup import MessageGroupPage
from pages.workbench.group_messenger.Organization import Organization
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage

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
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def enter_message_page():
        """进入到消息列表页面"""
        Preconditions.select_mobile('Android-移动', False)
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
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail():
            one_key.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)


# @unittest.skip
class MassMessengerTest(TestCase):
    """群发信使 模块"""

    def default_setUp(self):
        """确保进入消息列表页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        wp = WorkbenchPage()
        if wp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            wp.open_message_page()
            return
        else:
            current_mobile().reset_app()
            Preconditions.enter_message_page()

    def default_tearDown(self):
        pass

    @tags('ALL','workbench')
    def test_QFXS_0008(self):
        """1、点击用户本人头像"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        #点击群发信使
        wp.click_group_messenger()
        #等待页面加载
        mgp=MessageGroupPage()
        mgp.wait_for_page_load()
        #点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        #点击收件人
        mgp.click_addressee()
        #点击本机号码
        sccp=SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sccp.click_text(phone_number)
        if not sccp.is_toast_exist("该联系人不可选"):
            raise AssertionError("没有toast提示该联系人不可选")
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()

    @tags('ALL','workbench')
    def test_QFXS_0010(self):
        """1、搜索不存在的用户名称"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 点击群发信使
        wp.click_group_messenger()
        # 等待页面加载
        mgp = MessageGroupPage()
        mgp.wait_for_page_load()
        # 点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        # 点击收件人
        mgp.click_addressee()
        # 点击本机号码
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        #搜索框输入不存在用户名
        sccp.input_search_message("嗯嗯")
        if not sccp.is_toast_exist("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()

    @tags('ALL','workbench')
    def test_QFXS_0011(self):
        """1、再次点击头像，取消选择人员"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 点击组织架构，添加联系人
        wp.click_organization()
        org=Organization()
        org.wait_for_page_load()
        org.click_text("添加联系人")
        time.sleep(2)
        org.click_text("从手机通讯录添加")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_one_contact("和飞信电话")
        sccp.click_sure()
        org.wait_for_page_load()
        org.click_back()
        wp.wait_for_page_load()
        # 点击群发信使
        wp.click_group_messenger()
        # 等待页面加载
        mgp = MessageGroupPage()
        mgp.wait_for_page_load()
        # 点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        # 点击收件人
        mgp.click_addressee()
        # 点击指定联系人
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_text("和飞信电话")
        time.sleep(3)
        sccp.click_text("和飞信电话")
        if sccp.is_left_head_exit():
            raise AssertionError("搜索栏左侧被取消人员人名和头像没有被移除")
        #返回
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()

    @tags('ALL','workbench')
    def test_QFXS_0013(self):
        """1、点击“+”，添加接收人
            2、添加人数小于当前企业剩余条数"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 点击群发信使
        wp.click_group_messenger()
        # 等待页面加载
        mgp = MessageGroupPage()
        mgp.wait_for_page_load()
        # 点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        # 点击收件人
        mgp.click_addressee()
        # 点击指定联系人
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_text("和飞信电话")
        if not sccp.is_left_head_exit():
            raise AssertionError("找不到搜索栏左侧被点击人员人名和头像")
        #返回
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()