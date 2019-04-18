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
from pages.workbench.manager_console.ManagerGuide import ManagerGuidePage

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
    def enter_manager_guide_page():
        """进入管理员指引首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp = ManagerGuidePage()
        mgp.wait_for_page_load()


class MobileAttendanceAllTest(TestCase):
    """
    模块：工作台->管理员指引、权益
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->管理员指引、权益
    Author：刘晓东
    """

    def default_setUp(self):
        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0001(self):
        """能够正常打开管理员指引页面，可以正常返回"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        mgp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        # 1、2.进入各个指引页
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_back()
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_back()
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_back()
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_back()
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_back()
        mgp.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        # 3.进入帮助中心
        mgp.click_guide_by_name("帮助中心")
        mgp.wait_for_guide_page_load("创建团队")
        mgp.click_guide_by_name("员工手册")
        mgp.wait_for_guide_page_load("常见问题")
        mgp.click_guide_by_name("应用大全")
        mgp.wait_for_guide_page_load("和飞信特色通讯套件")
        mgp.click_guide_by_name("开发者文档")
        mgp.wait_for_guide_page_load("开发者接入")
        mgp.click_back()
        # 等待管理员指引首页加载
        mgp.wait_for_page_load()

