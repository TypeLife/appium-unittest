import unittest

import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import switch_to_mobile, current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage, SelectLocalContactsPage
from pages import GuidePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.group_messenger.GroupMessenger import GroupMessengerPage
from pages.workbench.group_messenger.HelpCenter import HelpCenterPage
from pages.workbench.group_messenger.MessageGroup import MessageGroupPage
from pages.workbench.group_messenger.NewMessage import NewMessagePage
from pages.workbench.group_messenger.Organization import Organization
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage

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
        login_num = Preconditions.login_by_one_key_login()
        return login_num

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_group_messenger_page():
        """进入群发信使首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_messenger_group()
        # 解决工作台不稳定问题
        if wbp.is_on_workbench_page():
            wbp.click_group_messenger()

    @staticmethod
    def create_he_contacts(names):
        """选择本地联系人创建为和通讯录联系人"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        time.sleep(2)
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
        import random
        a=str(random.random())
        #搜索框输入不存在用户名
        sccp.input_search_message(a)
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


class MassMessengerAllTest(TestCase):
    """
    模块：工作台->群发信使
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->群发信使
    Author：刘晓东
    """

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在群发信使首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_group_messenger_page()
            return
        gmp = GroupMessengerPage()
        if gmp.is_on_group_messenger_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            # preconditions.force_close_and_launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_messenger_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0001(self):
        """可以正常查看帮助中心内容"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        hcp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0005(self):
        """添加搜索出的联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exist_text(names[0]), True)
        nmp.click_back()
        time.sleep(2)
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0016(self):
        """搜索“我的电脑”"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        time.sleep(2)
        # 输入查找信息
        sccp.input_search_message("我的电脑")
        time.sleep(2)
        # 1.是否显示“无搜索结果”
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0017(self):
        """11位号码精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        time.sleep(2)
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(names[0])
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0018(self):
        """6-10位数字可支持模糊搜索匹配结果"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138"
        # 输入查找信息
        sccp.input_search_message(search_number)
        time.sleep(2)
        # 1.检查搜索结果是否模糊匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(names[0])
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0019(self):
        """联系人姓名（全名）精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(names[0])
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image(), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0020(self):
        """联系人姓名（非全名）模糊搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否模糊匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(names[0])
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image(), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0025(self):
        """纯空格键不支持搜索匹配"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_content = " "
        # 输入查找信息
        sccp.input_search_message(search_content)
        time.sleep(2)
        # 1.纯空格键不支持搜索匹配
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0030(self):
        """字母+汉字组合可精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["b测算", "大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "b测算"
        # 1.输入查找信息，检查搜索结果是否精准匹配关键字
        sccp.input_search_message(search_name)
        time.sleep(2)
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(names[0])
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("测算"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image(), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0031(self):
        """字母+汉字+数字 组合可精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["c平5", "大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "c平5"
        # 1.输入查找信息，检查搜索结果是否精准匹配关键字
        sccp.input_search_message(search_name)
        time.sleep(2)
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(names[0])
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("平5"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image(), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0032(self):
        """搜索非企业联系人提示无结果"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        time.sleep(2)
        # 输入不存在在企业通讯录中的用户电话号码
        sccp.input_search_message("13900009999")
        time.sleep(2)
        # 1.是否显示“无搜索结果”
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0033(self):
        """任意点击搜索结果联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人可供搜索
        gmp.click_back()
        names = ["大佬1", "大佬2"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        time.sleep(2)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 1.是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image(), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0035(self):
        """多选-任意选择多位联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人
        gmp.click_back()
        names = ["大佬1", "大佬2", "大佬3"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 选择三位联系人
        sccp.click_contacts_by_name(names[0])
        sccp.click_contacts_by_name(names[1])
        sccp.click_contacts_by_name(names[2])
        time.sleep(2)
        # 联系人是否为已选中状态
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 是否展示已选人数/上限人数
        self.assertEquals(sccp.is_exist_select_and_all("3"), True)
        # 取消已选联系人
        sccp.click_contacts_by_name(names[0])
        time.sleep(2)
        # 1.被取消联系人是否被移除，已选人数/上限人数是否改变
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), False)
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0039(self):
        """直接添加接收人后再次点击'+'"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保和通讯录有联系人
        gmp.click_back()
        names = ["大佬1", "大佬2", "大佬3"]
        Preconditions.create_he_contacts(names)
        wbp = WorkbenchPage()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 选择两位联系人
        sccp.click_contacts_by_name(names[0])
        sccp.click_contacts_by_name(names[1])
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp.wait_for_page_load()
        # 1.跳转联系人选择器后，上次添加的联系人是否为已选中状态
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        sccp.click_contacts_by_name(names[2])
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 2.是否添加成功，已添加与新添加用户均展示正常
        self.assertEquals(nmp.is_exist_text(names[0]), True)
        self.assertEquals(nmp.is_exist_text(names[1]), True)
        self.assertEquals(nmp.is_exist_text(names[2]), True)
        nmp.click_back()
        time.sleep(2)
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0042(self):
        """点击返回键返回上一级页面"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 返回上一级
        nmp.click_back()
        # 1.等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0043(self):
        """点击顶部关闭按钮退出到工作台页面"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保有【x】控件可点击
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_close()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_workbench_page_load()
        wbp.click_group_messenger()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
