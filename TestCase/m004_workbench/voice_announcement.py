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

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0003(self):
        """剩余条数显示正确"""
        # 1、查看本月剩余通知条数
        # 2、发送一条语音通知，选择1个成员
        # 3、查看本月剩余通知条数权益是否正常减去已发送的数量
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        if vnp.is_text_present("本月剩余通知 50 条"):
            #创建语音通知
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.input_notice_text("哈哈")
            time.sleep(2)
            vnp.click_add()
            sc = SelectContactsPage()
            sc.click_local_contacts()
            sc.click_one_contact("和飞信电话")
            time.sleep(2)
            sc.click_sure_bottom()
            time.sleep(2)
            vnp.click_send()
            vnp = VoiceNoticePage()
            vnp.wait_for_page_loads()
            if not vnp.is_text_present("本月剩余通知 49 条"):
                raise AssertionError("剩余条数无法正常减1")
        else:
            print("已创建通知")

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0005(self):
        """正常展开收起权益"""
        # 1、点击本月剩余通知条数旁边的下三角
        # 2、点击展开页面的上三角
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_text("本月剩余通知")
        time.sleep(2)
        if not vnp.is_text_present("企业认证"):
            raise AssertionError("不可正常展开")
        vnp.click_element_("上三角")
        time.sleep(2)
        if vnp.is_text_present("企业认证"):
            raise AssertionError("不可正常收起")

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0006(self):
        """跳转企业认证"""
        # 1、点击本月剩余通知条数旁边的下三角
        # 2、点击“企业认证”
        # 3、点击“马上去认证”
        # 4、点击复制地址
        # 5、点击【x】
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_text("本月剩余通知")
        time.sleep(2)
        vnp.click_text("企业认证")
        time.sleep(3)
        if not vnp.is_text_present("马上去认证"):
            raise AssertionError("不可正常进入企业认证详情页")
        vnp.click_text("马上去认证")
        time.sleep(2)
        if not vnp.is_text_present("如何申请认证"):
            raise AssertionError("没有弹出‘如何申请认证’弹窗")
        vnp.click_text("复制地址")
        if not vnp.is_toast_exist("复制成功"):
            raise AssertionError("没有弹出复制成功toast提示")
        time.sleep(3)
        vnp.click_text("马上去认证")
        time.sleep(2)
        vnp.click_element_("如何申请认证X号")
        time.sleep(1)
        if vnp.is_text_present("如何申请认证"):
            raise AssertionError("不可关闭弹窗")
        current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0007(self):
        """可正常跳转到充值页面"""
        # 1、点击本月剩余通知条数旁边的下三角
        # 2、点击“充值”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_text("本月剩余通知")
        time.sleep(2)
        vnp.click_text("充值")
        time.sleep(5)
        if not vnp.is_text_present("和飞信套餐"):
            raise AssertionError("不可正常跳转到充值页面")
        current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0008(self):
        """添加搜索出的成员"""
        # 1、点击“+”
        # 2、搜索关键词
        # 3、点击搜索结果中的成员
        # 4、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_text("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.input_search_keyword("和")
        time.sleep(2)
        vnp.click_text("和飞信电话")
        time.sleep(2)
        sc.click_sure_bottom()
        time.sleep(2)
        if not vnp.is_text_present("和飞信电话"):
            raise AssertionError("成员列表不能显示已勾选成员信息")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_00012(self):
        """无号码或自己等于100，成员等于20的时候成员不可勾选"""
        # 1、点击“+”
        # 2、选择无号码或自己等级 = 100
        # 时，成员等级等于20的用户
        # 3、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_text("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sc.click_one_contact(phone_number)
        if not vnp.is_toast_exist("该联系人不可选择"):
            raise AssertionError("没有提示“该联系人不可选”")
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_00014(self):
        """语音时长小于1s"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、按住话筒录制小于1s语音就松手
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_text("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.click_element_("语音话筒按钮")
        if vnp.is_text_present("始终允许"):
            vnp.click_text("始终允许")
            time.sleep(2)
            vnp.click_element_("语音话筒按钮")
        if not vnp.is_toast_exist("时间太短"):
            raise AssertionError("没有提示时间太短")
        current_mobile().back()
        current_mobile().back()
        vnp.wait_for_page_loads()

