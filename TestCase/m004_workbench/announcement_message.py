import unittest

from pages.workbench.announcement_message.AnnouncementMessage import AnnouncementMessagePage
from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.super_meeting.SuperMeeting import SuperMeetingPage
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

class AnnouncementMessageTest(TestCase):
    """
    模块：工作台->公告信息
    文件位置：20190313工作台全量用例整理.xlsx
    表格：公告信息
    """

    def default_setUp(self):
        """进入公告信息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC','workbench', 'GGXX')
    def test_GGXX_0001(self):
        """检查公告信息入口是否正确"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击公告信息应用图标
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        if not amp.is_text_present("未发公告"):
            raise AssertionError("不能正常进入公告信息首页")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0002(self):
        """检查点击返回按钮控件是否正确"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击【 < 】
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        time.sleep(3)
        amp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()





