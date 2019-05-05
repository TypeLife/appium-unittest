import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from pages import AgreementDetailPage
from pages import ContactsPage
from pages import GroupListPage
from pages import GuidePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import SelectLocalContactsPage
from pages import WorkbenchPage
from pages.workbench.app_manage.AppManage import AppManagePage
from pages.workbench.app_store.AppStore import AppStorePage
from pages.workbench.attendance_card.AttendanceCard import AttendanceCardPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from pages.workbench.manager_console.WorkbenchManage import WorkbenchManagePage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.super_meeting.SuperMeeting import SuperMeetingPage

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
    def enter_app_store_page():
        """进入应用商城首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()

    @staticmethod
    def ensure_not_exists_personal_app_by_name(name):
        """确保不存在指定个人应用"""

        wbp = WorkbenchPage()
        if wbp.is_exists_app_by_name(name):
            wbp.click_app_manage()
            amp = AppManagePage()
            # 解决工作台不稳定问题
            time.sleep(5)
            n = 1
            while amp.is_text_present("获取用户信息失败"):
                amp.click_back()
                wbp.wait_for_workbench_page_load()
                wbp.click_app_manage()
                time.sleep(5)
                n += 1
                if n > 10:
                    break
            amp.wait_for_page_load()
            amp.click_remove_icon_by_name(name)
            time.sleep(1)
            amp.click_sure()
            time.sleep(1)
            amp.click_back()
            wbp.wait_for_workbench_page_load()

    @staticmethod
    def ensure_not_exists_app_by_name(name):
        """确保不存在指定应用"""

        wbp = WorkbenchPage()
        if wbp.is_exists_app_by_name(name):
            wbp.click_workbench_manage()
            wmp = WorkbenchManagePage()
            wmp.wait_for_page_load()
            wmp.click_remove_icon_by_app_name(name)
            time.sleep(2)
            wmp.click_back()
            wbp.wait_for_workbench_page_load()

    @staticmethod
    def create_he_contacts(names):
        """选择手机联系人创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        time.sleep(5)
        n = 1
        # 解决工作台不稳定问题
        while osp.is_text_present("账号认证失败"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            time.sleep(5)
            n += 1
            if n > 10:
                break
        time.sleep(3)
        for name in names:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(2)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name(name)
                slc.click_sure()
                osp.wait_for_page_load()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_he_contacts2(contacts):
        """手动输入联系人创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        time.sleep(5)
        n = 1
        # 解决工作台不稳定问题
        while osp.is_text_present("账号认证失败"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            time.sleep(5)
            n += 1
            if n > 10:
                break
        time.sleep(3)
        for name, number in contacts:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(2)
                osp.click_specify_element_by_name("手动输入添加")
                osp.input_contacts_name(name)
                osp.input_contacts_number(number)
                osp.click_confirm()
                osp.wait_for_page_load()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_department_and_add_member(department_names):
        """创建企业部门并从手机联系人添加成员"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        time.sleep(5)
        n = 1
        # 解决工作台不稳定问题
        while osp.is_text_present("账号认证失败"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            time.sleep(5)
            n += 1
            if n > 10:
                break
        time.sleep(3)
        for department_name in department_names:
            if not osp.is_exist_specify_element_by_name(department_name):
                osp.click_specify_element_by_name("添加子部门")
                time.sleep(2)
                osp.input_sub_department_name(department_name)
                osp.input_sub_department_sort("1")
                osp.click_confirm()
                if osp.is_toast_exist("部门已存在", 2):
                    osp.click_back()
                osp.wait_for_page_load()
                osp.click_specify_element_by_name(department_name)
                time.sleep(2)
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(2)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name("大佬1")
                slc.selecting_local_contacts_by_name("大佬2")
                slc.selecting_local_contacts_by_name("大佬3")
                slc.selecting_local_contacts_by_name("大佬4")
                slc.click_sure()
                osp.wait_for_page_load()
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()


class AppStoreAllTest(TestCase):
    """
    模块：工作台->应用商城
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->应用商城
    Author：刘晓东
    """

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

        # 导入团队联系人、企业部门
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海贵', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                department_names = ["测试部门1", "测试部门2"]
                Preconditions.create_department_and_add_member(department_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

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
        acp = AttendanceCardPage()
        if acp.is_on_attendance_card_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0001(self):
        """检查工作台进入应用商城入口是否正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        # 1.等待应用商城首页加载
        asp.wait_for_page_load()
        asp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0002(self):
        """检查【>】返回按钮控件是否正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        asp.click_back()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0003(self):
        """搜索未添加个人应用添加"""

        # 确保不存在指定个人应用
        app_name = "咪咕影院"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击搜索应用
        asp.click_search_app()
        # 1.等待搜索页加载
        asp.wait_for_search_page_load()
        asp.input_store_name(app_name)
        time.sleep(1)
        # 2.搜索栏是否显示指定文本
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_search()
        time.sleep(5)
        # 解决工作台不稳定的问题
        if not asp.is_exist_join():
            asp.click_close()
            wbp.wait_for_workbench_page_load()
            wbp.click_app_store()
            asp.wait_for_page_load()
            asp.click_search_app()
            asp.wait_for_search_page_load()
            asp.input_store_name(app_name)
            asp.click_search()
            time.sleep(5)
        # 3.搜索关键词是否展示在搜索结果列表中
        self.assertEquals(asp.is_search_result_match(app_name), True)
        # 4.点击添加
        asp.click_join()
        time.sleep(2)
        asp.click_sure()
        # 5.添加成功，返回搜索页，搜索栏是否清空
        asp.wait_for_search_page_load()
        self.assertEquals(asp.get_search_box_text(), "")
        asp.click_close()
        wbp.wait_for_workbench_page_load()
        # 6.工作台新增个人应用分组，是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0004(self):
        """搜索未添加个人应用进入应用介绍页添加"""

        # 确保不存在指定个人应用
        app_name = "网易考拉"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击搜索应用
        asp.click_search_app()
        # 1.等待搜索页加载
        asp.wait_for_search_page_load()
        asp.input_store_name(app_name)
        time.sleep(1)
        # 2.搜索栏是否显示指定文本
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_search()
        time.sleep(5)
        # 解决工作台不稳定的问题
        if not asp.is_exist_join():
            asp.click_close()
            wbp.wait_for_workbench_page_load()
            wbp.click_app_store()
            asp.wait_for_page_load()
            asp.click_search_app()
            asp.wait_for_search_page_load()
            asp.input_store_name(app_name)
            asp.click_search()
            time.sleep(5)
        # 3.搜索关键词是否展示在搜索结果列表中
        self.assertEquals(asp.is_search_result_match(app_name), True)
        # 进入应用介绍页
        asp.click_search_result()
        # 4.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        # 5.点击添加
        asp.click_join()
        time.sleep(2)
        asp.click_sure()
        asp.click_back()
        time.sleep(2)
        # 6.添加成功，返回搜索页，搜索栏内容保存
        asp.wait_for_search_page_load()
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_close()
        wbp.wait_for_workbench_page_load()
        # 7.工作台新增个人应用分组，是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0007(self):
        """个人专区添加应用"""

        # 确保不存在指定个人应用
        app_name = "帮助中心"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.点击个人专区
        asp.click_personal_area()
        time.sleep(5)
        # 2.添加指定应用
        asp.add_app_by_name(app_name)
        asp.click_sure()
        time.sleep(5)
        # 3.添加按钮是否变化为打开按钮
        self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_back()
        wbp.wait_for_workbench_page_load()
        # 4.工作台新增个人应用分组，是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0008(self):
        """个人专区进入应用介绍页添加应用"""

        # 确保不存在指定个人应用
        app_name = "政企优惠"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.点击个人专区
        asp.click_personal_area()
        time.sleep(5)
        # 进入应用介绍页
        asp.click_text(app_name)
        # 2.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        # 3.点击添加
        asp.click_join()
        time.sleep(1)
        asp.click_sure()
        time.sleep(1)
        asp.click_back()
        time.sleep(5)
        # 4.添加按钮是否变化为打开按钮
        self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_back()
        wbp.wait_for_workbench_page_load()
        # 5.工作台新增个人应用分组，是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    # @tags('ALL', 'CMCC', 'workbench', 'LXD')
    # def test_YYSC_0011(self):
    #     """管理员搜索未添加企业应用时添加"""
    #
    #     # 确保不存在指定应用
    #     app_name = "人事管理"
    #     Preconditions.ensure_not_exists_app_by_name(app_name)
    #     # 添加工作台里的应用
    #     wbp = WorkbenchPage()
    #     wbp.click_app_store()
    #     asp = AppStorePage()
    #     asp.wait_for_page_load()
    #     # 点击搜索应用
    #     asp.click_search_app()
    #     # 1.等待搜索页加载
    #     asp.wait_for_search_page_load()
    #     asp.input_store_name(app_name)
    #     time.sleep(1)
    #     # 2.搜索栏是否显示指定文本
    #     self.assertEquals(asp.get_search_box_text(), app_name)
    #     asp.click_search()
    #     time.sleep(5)
    #     # 解决工作台不稳定的问题
    #     if not asp.is_exist_join():
    #         asp.click_close()
    #         wbp.wait_for_workbench_page_load()
    #         wbp.click_app_store()
    #         asp.wait_for_page_load()
    #         asp.click_search_app()
    #         asp.wait_for_search_page_load()
    #         asp.input_store_name(app_name)
    #         asp.click_search()
    #         time.sleep(5)
    #     # 3.搜索关键词是否展示在搜索结果列表中
    #     self.assertEquals(asp.is_search_result_match(app_name), True)
    #     # 4.点击添加
    #     asp.click_join()
    #     time.sleep(2)
    #     # 5.选择应用分组（勾选状态没有可辨识标识，无法验证）
    #     asp.click_text("团队沟通")
    #     time.sleep(2)
    #     asp.click_add_app()
    #     time.sleep(2)
    #     # 进入移动办公套件应用列表
    #     asp.click_back()
    #     asp.wait_for_page_load()
    #     asp.click_text("分类")
    #     time.sleep(2)
    #     asp.click_text("移动办公套件")
    #     time.sleep(2)
    #     # 6.添加按钮是否变化为打开按钮
    #     self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
    #     asp.click_back()
    #     time.sleep(1)
    #     asp.click_back()
    #     wbp.wait_for_workbench_page_load()
    #     # 7.工作台是否存在指定应用图标
    #     self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0015(self):
        """验证brenner图>1时是否正常切换"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.滑动brenner图
        asp.swipe_by_brenner1()
        time.sleep(1)
        asp.swipe_by_brenner2()
        asp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0016(self):
        """验证点击brenner图是否跳转正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击brenner图
        asp.click_brenner()
        # 1.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        asp.click_back()
        asp.wait_for_page_load()
        asp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0018(self):
        """检查【X】返回按钮控件是否正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 进入应用商城二三级页面
        asp.click_text("超级会议")
        asp.wait_for_app_details_page_load()
        asp.click_close()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0019(self):
        """验证点击打开按钮是否跳转正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        wbp = WorkbenchPage()
        asp.wait_for_page_load()
        # 搜索应用
        asp.click_search_app()
        search_name = "企业通讯录"
        asp.wait_for_search_page_load()
        asp.input_store_name(search_name)
        time.sleep(1)
        asp.click_search()
        time.sleep(5)
        # 解决工作台不稳定的问题
        if not asp.is_exist_join():
            asp.click_close()
            wbp.wait_for_workbench_page_load()
            wbp.click_app_store()
            asp.wait_for_page_load()
            asp.click_search_app()
            asp.wait_for_search_page_load()
            asp.input_store_name(search_name)
            asp.click_search()
            time.sleep(5)
        # 打开应用
        asp.click_open()
        # 1.等待企业通讯录首页加载
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        asp.wait_for_search_page_load()
        asp.click_back()
        asp.wait_for_page_load()
        # 进入应用介绍页
        asp.click_text("超级会议")
        asp.wait_for_app_details_page_load()
        # 打开应用
        asp.click_open()
        smp = SuperMeetingPage()
        # 2.等待超级会议首页加载
        smp.wait_for_page_loads()
        smp.click_close()
        wbp.wait_for_workbench_page_load()