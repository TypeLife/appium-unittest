import unittest

from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import *
import time

from pages.workbench.create_team.CreateTeam import CreateTeamPage
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from TestCase.m001_login.login import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass

class VoiceAnnouncementTest(TestCase):
    """
    模块：工作台->语音通知
    文件位置：20190313工作台全量用例整理.xlsx
    表格：语音通知
    """

    def default_setUp(self):
        """进入语音通知页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_voice_announcement_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_voice_announcement_page()
            return
        vnp = VoiceNoticePage()
        if vnp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_voice_announcement_page()

    def default_tearDown(self):
        pass

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0001(self):
        """网络正常情况下正常跳转到应用首页"""
        # 1、点击【语音通知】
        # 2、查看跳转页面
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0002(self):
        """网络异常情况下提示页面"""
        # 1、断开网络
        # 2、点击【语音通知】
        # 3、查看跳转页面
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.set_network_status(0)
        time.sleep(8)
        workbench.click_voice_notice()
        time.sleep(2)
        if not vnp.is_text_present("网络出错，轻触屏幕重新加载"):
            raise AssertionError("没有出现‘网络出错，轻触屏幕重新加载’")
        vnp.click_text("网络出错，轻触屏幕重新加载")
        if not vnp.is_toast_exist("网络不可用，请检查网络设置"):
            raise AssertionError("没有出现‘网络不可用，请检查网络设置’toast提示")
        time.sleep(2)
        current_mobile().back()

    def tearDown_test_YYTZ_0002(self):
        # 重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(8)


