import unittest

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

class SuperMeetingTest(TestCase):
    """
    模块：工作台->超级会议
    文件位置：20190313工作台全量用例整理.xlsx
    表格：超级会议
    """

    def default_setUp(self):
        """进入超级会议页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_super_meeting_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_super_meeting_page()
            return
        smp = SuperMeetingPage()
        if smp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_super_meeting_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'workbench', 'CJHY')
    def test_CJHY_0001(self):
        """查看超级会议使用说明"""
        # 1、点击超级会议顶部下拉箭头
        # 2、点击“使用指南”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        # 1.点击点击右上角【？】
        smp.click_element_('？')
        smp.wait_for_page_loads("发起超级会议")
        # 2.上下滑动浏览页面
        a=0
        while a<10:
            smp.page_up()
            a+=1
        if not smp.is_text_present("时长权益扣减说明"):
            raise AssertionError("不可正常浏览页面")
        smp.click_close_more()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'workbench', 'CJHY')
    def test_CJHY_0002(self):
        """添加搜索出的企业通讯录联系人"""
        # 1、点击“预约会议”
        # 2、搜索关键词，如“测试”
        # 3、选择“搜索企业通讯录联系人：测试
        # 4、点击搜索出的成员
        # 5、点击“确定”
        # 6、选择开始时间，点击“下一步”
        # 7、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        else:
            current_mobile().back()
            wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_text("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        sc.input_search_contact_message("yyx")
        time.sleep(2)
        sc.click_text("18920736596")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(2)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        current_mobile().back()
        wbp.wait_for_page_load()

