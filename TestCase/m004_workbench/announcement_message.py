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

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0003(self):
        """检查点击关闭按钮控件【X】"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击【x】
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        time.sleep(3)
        amp.click_text("发布公告")
        time.sleep(2)
        amp.click_element_("X")
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0004(self):
        """管理员进入发布公告，检查初始化页面"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】初始化页面
        # 3、检查【公告信息】初始化页面
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        time.sleep(2)
        if not amp.is_text_present("向团队所有成员发出第一条公告"):
            raise AssertionError("没有出现初始化页面显示文字")
        if not amp.is_text_present("发布公告"):
            raise AssertionError("没有发布公告按钮")
        if not amp.is_text_present("未发公告"):
            raise AssertionError("没有未发公告按钮")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0006(self):
        """管理员进入发布公告，公告搜索-按中文搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按中文搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_text("发布公告")
        time.sleep(2)
        amp.input_title_text("哈哈")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("哈")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("哈哈"):
            raise AssertionError("搜索不成功")
        amp.click_text("哈哈")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0007(self):
        """管理员进入发布公告，公告搜索-按英文搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按英文搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_text("发布公告")
        time.sleep(2)
        amp.input_title_text("hello")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("hel")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("hello"):
            raise AssertionError("搜索不成功")
        amp.click_text("hello")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0008(self):
        """管理员进入发布公告，公告搜索-按特殊字符搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按特殊字符搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha*")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("*")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha*"):
            raise AssertionError("搜索不成功")
        amp.click_text("ha*")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

