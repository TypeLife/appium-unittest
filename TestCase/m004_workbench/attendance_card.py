import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from pages import AgreementDetailPage
from pages import GuidePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import WorkbenchPage
from pages.workbench.attendance_card.AttendanceCard import AttendanceCardPage

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

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def enter_attendance_card_page():
        """进入考勤打卡首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_add_attendance_card()

    @staticmethod
    def create_attendance_group():
        """创建考勤组"""

        acp = AttendanceCardPage()
        acp.click_text("新建考勤组")
        time.sleep(3)
        acp.click_text("请选择")
        time.sleep(1)
        acp.click_text("全选")
        time.sleep(1)
        acp.click_text("确认")
        time.sleep(1)
        acp.click_create_attendance_group_button()
        time.sleep(5)
        acp.click_back()


class AttendanceCardAllTest(TestCase):
    """
    模块：工作台->考勤打卡
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->考勤打卡
    Author：刘晓东
    """

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在工作台首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_workbench_page()
            return
        wbp = WorkbenchPage()
        if wbp.is_on_workbench_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_KQDK_0001(self):
        """帮助文档展示正常"""

        # 进入考勤打卡首页
        Preconditions.enter_attendance_card_page()
        acp = AttendanceCardPage()
        acp.wait_for_page_load()
        wbp = WorkbenchPage()
        # # 解决工作台不稳定问题
        # acp.click_back()
        # wbp.wait_for_workbench_page_load()
        # wbp.click_attendance_card()
        # acp.wait_for_page_load()
        time.sleep(10)
        # 确保已经加入考勤组
        if acp.is_text_present("新建考勤组"):
            Preconditions.create_attendance_group()
        time.sleep(2)
        # 点击帮助图标
        acp.click_help_icon()
        time.sleep(2)
        # 1.进入各个帮助页
        acp.click_text("获取地址失败")
        acp.wait_for_help_page_load("获取地址失败")
        acp.click_back()
        time.sleep(1)
        acp.click_text("定位不准确")
        acp.wait_for_help_page_load("定位不准确")
        acp.click_back()
        time.sleep(1)
        acp.click_text("提示不在考勤组")
        acp.wait_for_help_page_load("提示不在考勤组")
        acp.click_back()
        time.sleep(1)
        acp.click_back()
        time.sleep(1)
        acp.click_back()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_KQDK_0006(self):
        """点击顶部返回键，返回到上一级页面"""

        # 进入考勤打卡首页
        Preconditions.enter_attendance_card_page()
        acp = AttendanceCardPage()
        acp.wait_for_page_load()
        time.sleep(10)
        # 确保已经加入考勤组
        if acp.is_text_present("新建考勤组"):
            Preconditions.create_attendance_group()
        time.sleep(2)
        acp.click_back()
        wbp = WorkbenchPage()
        # 1.等待工作台首页加载
        wbp.wait_for_workbench_page_load()




