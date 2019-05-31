import unittest
import uuid
import time
import threading
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.SelectHeContacts import SelectHeContactsPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage

REQUIRED_MOBILES = {
    'Android-移动':'M960BDQN229CH',
    'Android-移动2':'M960BDQN229CK_20',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """
    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def create_contacts(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        contact_search.click_back()
        contacts_page.click_add()
        create_page = CreateContactPage()
        create_page.hide_keyboard_if_display()
        create_page.create_contact(name, number)
        detail_page.wait_for_page_load()
        detail_page.click_back_icon()

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)

    @staticmethod
    def create_contacts_if_not_exits(name, number):
        """
        不存在就导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        if contact_search.is_contact_in_list(name):
            contact_search.click_back()
        else:
            contact_search.click_back()
            contacts_page.click_add()
            create_page = CreateContactPage()
            create_page.hide_keyboard_if_display()
            create_page.create_contact(name, number)
            detail_page.wait_for_page_load()
            detail_page.click_back_icon()

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
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name in names:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name(name)
                slc.click_sure()
                time.sleep(2)
                osp.click_back()
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
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name, number in contacts:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("手动输入添加")
                osp.input_contacts_name(name)
                osp.input_contacts_number(number)
                osp.click_confirm()
                time.sleep(2)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_sub_department_by_name(departmentName,name):
        """从消息列表开始创建子部门并添加一个部门成员"""
        WorkbenchPreconditions.enter_organization_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if osp.is_element_present_by_name(departmentName):
            time.sleep(2)
        else:
            osp.click_text("添加子部门")
            osp.wait_for_sub_department_page_load()
            osp.input_sub_department_name(departmentName)
            osp.click_text("完成")
            time.sleep(2)
        osp.click_text(departmentName)
        time.sleep(2)
        if osp.is_element_present_by_name(name):
            time.sleep(2)
        else:
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            slc = SelectLocalContactsPage()
            # 选择联系人
            names=slc.get_contacts_name_list()
            time.sleep(2)
            sc.click_one_contact(name)
            # sc.click_one_contact(name)
            # sc.click_one_contact(name)
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("操作成功"):
                raise AssertionError("操作不成功")
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        if not osp.is_on_this_page():
            raise AssertionError("没有返回上一级")
        time.sleep(2)
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        time.sleep(3)
        current_mobile().back()
        workbench.open_message_page()


class GroupcontactsSelectPage(TestCase):
    """
    模块:通讯录--企业联系人选择器
    """
    def default_setUp(self):
        """确保每个用例执行前在通讯录页面"""
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_add_icon()
        MessagePage().click_new_message()
        time.sleep(2)
        SelectContactsPage().click_group_contact()
        time.sleep(3)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0732(self):
        """顶部标题为：选择联系人"""
        select_group_contact=SelectHeContactsPage()
        title=select_group_contact.get_element_text(locator='选择联系人')
        self.assertEqual(title,'选择联系人')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0769(self):
        """搜索框默认提示语修改为：搜索或输入手机号"""
        select_group_contact=SelectHeContactsPage()
        title=select_group_contact.get_element_text(locator='搜索或输入手机号')
        self.assertEqual(title,'搜索或输入手机号')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0770(self):
        """点击搜索框，光标在搜索框时自动弹出键盘，点击其他区域后，键盘自动收起"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        select_group_contact.is_keyboard_shown()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0771(self):
        """进入搜索状态，搜索框默认提示语“搜索”[搜索框文本应该为:搜索或输入手机号]"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        select_group_contact.input_search_keywords('大佬')
        time.sleep(2)
        select_group_contact.clear_input_box()
        text=select_group_contact.get_element_text('搜索或输入手机号')
        self.assertEqual(text,'搜索或输入手机号')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0772(self):
        """输入框为空时，右侧不显示 一键消除 X 按钮"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        self.assertFalse(select_group_contact.is_element_present(locator='清空搜索框'))

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0773(self):
        """输入框有内容时，右侧显示 一键消除 X 按钮，点击X可清空内容"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        text='测试'
        select_group_contact.input_search_keywords(text)
        self.assertTrue(select_group_contact.is_element_present(locator='清空搜索框'))
        time.sleep(2)
        select_group_contact.clear_input_box()
        text2 = select_group_contact.get_element_text('搜索或输入手机号')
        self.assertNotEqual(text, text2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0724(self):
        """测试搜索输入框的X按钮是否可以清空内容"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        text='测试'
        select_group_contact.input_search_keywords(text)
        time.sleep(2)
        select_group_contact.clear_input_box()
        text2 = select_group_contact.get_element_text('搜索或输入手机号')
        self.assertNotEqual(text, text2)


