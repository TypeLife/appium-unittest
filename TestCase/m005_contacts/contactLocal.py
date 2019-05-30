import unittest
import uuid
import time
import threading
from preconditions.BasePreconditions import LoginPreconditions
from library.core.mobile.mobiledriver import MobileDriver
from selenium.common.exceptions import TimeoutException
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.HeContacts import HeContactsPage
from pages.contacts.official_account import OfficialAccountPage
from pages.contacts.search_official_account import SearchOfficialAccountPage
from pages.contacts.official_account_detail import OfficialAccountDetailPage
from pages.contacts.EditContactPage import EditContactPage
from pages.contacts.components.menu_more import MenuMore
from pages.contacts.local_contact import localContactPage
import preconditions
from dataproviders import contact2
from pages.message.MassAssistant import Massassistant


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

@unittest.skip("本地调试不执行")
class ContactLocal(TestCase):
    """
    模块：联系-本地联系人
    文件位置：全量/115全量测试用例-联系(1322).xlsx--高等级用例(优先编写)
    表格：通讯录-本地通讯录
    author: 余梦思
    """
    # @classmethod
    # def setUpClass(cls):
    #     # 创建联系人
    #     fail_time = 0
    #     import dataproviders
    #
    #     while fail_time < 3:
    #         try:
    #             # 获取需要导入的联系人数据
    #           #  required_contacts = dataproviders.get_preset_contacts()
    #             required_contacts =contact2.get_preset_contacts()
    #
    #             # 连接手机
    #             Preconditions.connect_mobile('Android-移动')
    #             current_mobile().hide_keyboard_if_display()
    #             # 导入数据
    #             for name, number in required_contacts:
    #                 Preconditions.create_contacts(name, number)
    #
    #             # 推送resource文件到手机
    #             dataproviders.push_resource_dir_to_mobile_sdcard(Preconditions.connect_mobile('Android-移动'))
    #             return
    #         except:
    #             fail_time += 1
    #             import traceback
    #             msg = traceback.format_exc()
    #             print(msg)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     try:
    #         Preconditions.connect_mobile('Android-移动')
    #         current_mobile().hide_keyboard_if_display()
    #         Preconditions.make_already_in_message_page()
    #         conts_page = ContactsPage()
    #         conts_page.open_contacts_page()
    #         conts_page.click_label_grouping()
    #         lg = LabelGroupingPage()
    #         lg.wait_for_page_load()
    #         lg.delete_all_label()
    #     except:
    #         import traceback
    #         traceback.print_exc()
    #     try:
    #         current_mobile().hide_keyboard_if_display()
    #         Preconditions.make_already_in_message_page()
    #         cdp = ContactDetailsPage()
    #         cdp.delete_all_contact()
    #     except:
    #         traceback.print_exc()


class ContactsLocal(TestCase):
    """通讯录测试记录-陈继祥"""

    @classmethod
    def setUpClass(cls):
        # 创建联系人
        fail_time = 0
        import dataproviders

        while fail_time < 3:
            try:
                # 获取需要导入的联系人数据
                required_contacts = contact2.get_preset_contacts()

                # 连接手机
                Preconditions.connect_mobile('Android-移动')
                Preconditions.make_already_in_message_page()
                current_mobile().hide_keyboard_if_display()
                conts = ContactsPage()
                conts.open_contacts_page()
                # 导入数据
                for name, number in required_contacts:
                    # Preconditions.create_contacts_if_not_exits(name, number)
                    Preconditions.create_contacts_if_not_exits(name, number)

                # # 推送resource文件到手机
                # dataproviders.push_resource_dir_to_mobile_sdcard(Preconditions.connect_mobile('Android-移动'))
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    def default_setUp(self):
        """确保每个用例运行前在通讯录页面"""
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0001(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入数字模糊查询（只搜索一条记录）
        author:darcy

        :return:
        '''
        lcontact=localContactPage()
        lcontact.click_search_box()
        time.sleep(2)
        lcontact.input_search_text(text='138006')
        lcontact.hide_keyboard()
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0002(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入数字模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='138')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els=lcontact.get_element_number()
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0003(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入手机号码全匹配查询
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='13800138001')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')

    @staticmethod
    def setUp_test_contacts_chenjixiang_0019():
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().open_me_page()
        me_page = MePage()
        # me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0019(self):
        '''
       测试sim单卡测试，无联系人，手机系统设置关闭“显示SIM联系人”，和飞信关闭“显示sim卡联系人”，是否能搜索到本地联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("张无忌")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无搜索结果")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0020():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=True)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0020(self):
        '''
       测试sim单卡测试，有联系人，手机系统设置开启“显示SIM联系人”，和飞信开启“显示sim卡联系人”，是否能搜索到sim联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("大佬")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        time.sleep(1)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')

    @staticmethod
    def setUp_test_contacts_chenjixiang_0021():
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().open_me_page()
        me_page = MePage()
        # me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0021(self):
        '''
       测试sim单卡测试，有联系人，手机系统设置开启“显示SIM联系人”，和飞信关闭“显示sim卡联系人”，是否能搜索到sim联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("ximi")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        lcontact.is_text_present("无搜索结果")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0022():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        # time.sleep(3)
        # preconditions.launch_app()
        # time.sleep(1)
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=True)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0022(self):
        '''
       测试sim单卡，有联系人，手机系统设置关闭“显示SIM联系人”，和飞信开启“显示sim卡联系人”，是否能搜索到sim联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("大佬")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0005(self):
        '''
        搜索输入框校验，通过名称搜索（英文），输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='dalao')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0006(self):
        '''
        搜索输入框校验，通过名称搜索（特殊字符）,输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='#')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0004(self):
        '''
        搜索输入框校验，通过名称（中文）搜索，输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='大佬')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0008(self):
        '''
        测试空格+文本进行搜索
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='大佬  ')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0010(self):
        '''
        测试搜索输入框输入超长字符
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        lcontact.click_search_box()
        time.sleep(1)
        name='aa'*100
        lcontact.input_search_text(text=name)
        time.sleep(1)
        lcontact.hide_keyboard()
        text=lcontact.get_input_box_text()
        time.sleep(1)
        self.assertEqual(name,text)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0012(self):
        '''
        测试搜索输入框的X按钮是否可以清空内容
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        name = 'aa' * 100
        lcontact.input_search_text(text=name)
        lcontact.click_delete_button()
        time.sleep(2)
        lcontact.is_text_present("搜索")

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0014(self):
        '''
        搜索一个不存在本地的正常的11位号码
        auther:darcy
        :return:

        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410889633")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无搜索结果")

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0015(self):
        '''
        搜索不存在本地通讯录的联系人
        auther:darcy
        :return:

        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410889633")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无搜索结果")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0016():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact()
        time.sleep(5)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0016(self):
        '''
        测试sim单卡测试，无联系人，手机系统设置开启“显示SIM联系人”，和飞信开启“显示sim卡联系人”，是否能搜索到本地联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("dalao")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @staticmethod
    def setUp_test_contacts_chenjixiang_0017():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        time.sleep(2)
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0017(self):
        '''
       测试sim单卡测试，无联系人，手机系统设置开启“显示SIM联系人”，和飞信关闭“显示sim卡联系人”，是否能搜索到不存在的联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("张无忌")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无搜索结果")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0018():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=True)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0018(self):
        '''
       测试sim单卡测试，无联系人，手机系统设置关闭“显示SIM联系人”，和飞信开启“显示sim卡联系人”，是否能搜索到本地联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("dalao")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @staticmethod
    def setUp_test_contacts_chenjixiang_0023():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0023(self):
        '''
       测试sim单卡，有联系人，手机系统设置关闭“显示SIM联系人”，和飞信关闭“显示sim卡联系人”，是否能搜索到sim联系人
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("dalao")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无搜索结果")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0024():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC-双卡,跳过')
    def test_contacts_chenjixiang_0024(self):
        '''
       测试sim双卡，卡1有联系人，卡2无联系人，已开启“显示sim卡联系人”，分别搜索卡1、卡2、本地通讯录、和通讯录
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xiaomi")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无搜索结果")

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0030(self):
        '''
       测试搜索结果点击后跳转到profile页面
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("dalao4")
        time.sleep(1)
        lcontact.hide_keyboard()
        lcontact.click_text("大佬4")
        time.sleep(2)
        els=lcontact.get_element_number(text="dalao4")
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0031(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码不一致的情况，通过名称搜索
        auther:darcy
        :return:
        '''
        # 添加手机联系人
        time.sleep(2)
        # 添加联系人
        ContactsPage().click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('13410669625')
        if contact_search.is_exist_contacts():
            contact_search.click_back()
        else:
            contact_search.click_back()
            ContactsPage().click_add()
            creat_contact = CreateContactPage()
            creat_contact.click_input_name()
            creat_contact.input_name('xili')
            creat_contact.click_input_number()
            creat_contact.input_number('13410669625')
            creat_contact.click_save()
            time.sleep(2)
            ContactDetailsPage().click_back()
            time.sleep(2)

        lcontact = localContactPage()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(2)
        els=lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        time.sleep(1)
        lcontact.is_text_present("13410669632")
        lcontact.is_text_present("13410669625")

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0032(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码不一致的情况，通过手机号码搜索
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669632")
        lcontact.hide_keyboard()
        time.sleep(2)
        lcontact.is_text_present("xili")


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0033(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码一致的情况，通过名称搜索
        :return:
        '''
        # 添加手机联系人
        time.sleep(2)
        # 添加联系人
        ContactsPage().click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('13410669625')
        els = localContactPage().get_element_number()
        if len(els) > 1:
            contact_search.click_back()
        else:
            contact_search.click_back()
            ContactsPage().click_add()
            creat_contact = CreateContactPage()
            creat_contact.click_input_name()
            creat_contact.input_name('xili')
            creat_contact.click_input_number()
            creat_contact.input_number('13410669625')
            creat_contact.click_save()
            time.sleep(2)
            ContactDetailsPage().click_back()
            time.sleep(2)

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        time.sleep(2)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669625")
        lcontact.hide_keyboard()
        time.sleep(2)
        #显示多条结果，姓名,头像、手机号码一样
        els = lcontact.get_element_number()
        self.assertTrue(len(els) == 2)
        name1=lcontact.get_all_contacts_name()[0].text
        name2 = lcontact.get_all_contacts_name()[1].text
        self.assertEqual(name1,name2)
        time.sleep(1)
        number1 = lcontact.get_all_contacts_number()[0].text
        number2 = lcontact.get_all_contacts_number()[1].text
        self.assertEqual(number1, number2)
        time.sleep(1)
        #联系人头像是否一样无法判断
        # head1=lcontact.get_all_contacts_head()[0].text
        # head2 = lcontact.get_all_contacts_head()[1].text
        # self.assertEqual(head1,head2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0034(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码一致的情况，通过手机号码搜索
        :return:
        '''
        # 添加手机联系人
        time.sleep(2)
        # 添加联系人
        ContactsPage().click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('13410669616')
        els = localContactPage().get_element_number()
        if len(els) > 1:
            contact_search.click_back()
        else:
            contact_search.click_back()
            ContactsPage().click_add()
            creat_contact = CreateContactPage()
            creat_contact.click_input_name()
            creat_contact.input_name('xili')
            creat_contact.click_input_number()
            creat_contact.input_number('13410669616')
            creat_contact.click_save()
            time.sleep(2)
            ContactDetailsPage().click_back()
            time.sleep(2)

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        time.sleep(2)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669616")
        lcontact.hide_keyboard()
        time.sleep(2)
        #显示多条结果，姓名不一样，头像、手机号码一样
        els = lcontact.get_element_number()
        self.assertTrue(len(els) == 2)
        name1=lcontact.get_all_contacts_name()[0].text
        name2 = lcontact.get_all_contacts_name()[1].text
        self.assertNotEqual(name1,name2)
        time.sleep(1)
        number1 = lcontact.get_all_contacts_number()[0].text
        number2 = lcontact.get_all_contacts_number()[1].text
        self.assertEqual(number1, number2)
        time.sleep(1)
        # 联系人头像是否一样无法判断
        # head1=lcontact.get_all_contacts_head()[0]
        # head2 = lcontact.get_all_contacts_head()[1]
        # self.assertEqual(head1,head2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0035(self):
        '''
       测试系统通讯录存在多个联系人，名称相同，手机号码不一致，通过名称搜索
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(2)
        #显示多条结果，姓名一样，头像、手机号码不一样
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)
        name1=lcontact.get_all_contacts_name()[0].text
        name2 = lcontact.get_all_contacts_name()[1].text
        self.assertEqual(name1,name2)
        time.sleep(1)
        number1 = lcontact.get_all_contacts_number()[0].text
        number2 = lcontact.get_all_contacts_number()[1].text
        self.assertNotEqual(number1, number2)
        time.sleep(1)
        # 联系人头像是否一样无法判断
        # head1=lcontact.get_all_contacts_head()[0]
        # head2 = lcontact.get_all_contacts_head()[1]
        # self.assertNotEqual(head1,head2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0036(self):
        '''
       测试系统通讯录存在多个联系人，名称相同，手机号码不一致，通过手机号码搜索
        :return:
        '''

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # time.sleep(3)
        # GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669632")
        lcontact.hide_keyboard()
        time.sleep(2)
        lcontact.is_text_present("xili")
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')
        lcontact.click_back_by_android()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0039(self):
        '''
       测试系统通讯录存在多个联系人，名称不一致，手机号码相同，通过名称搜索
        :return:
        '''

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # time.sleep(3)
        # GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xihua")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xihua")
        time.sleep(1)
        lcontact.click_text("xihua")
        time.sleep(1)
        lcontact.is_text_present("xihua")
        lcontact.is_text_present("134 1066 9616")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0040(self):
        '''
       测试系统通讯录存在多个联系人，名称不一致，手机号码相同，通过手机号码搜索
        :return:
        '''

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # time.sleep(3)
        # GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669616")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xihua")
        time.sleep(1)
        lcontact.click_text("xihua")
        time.sleep(1)
        lcontact.is_text_present("xihua")
        lcontact.is_text_present("134 1066 9616")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0041(self):
        '''
       测试系统通讯录存在多个联系人，名称和手机号码不一致，通过名称搜索
        :return:
        '''

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # time.sleep(3)
        # GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("给个红包1")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("给个红包1")
        time.sleep(1)
        lcontact.click_text("给个红包1")
        time.sleep(1)
        lcontact.is_text_present("给个红包1")
        lcontact.is_text_present("13800138000")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0042(self):
        '''
       测试系统通讯录存在多个联系人，名称和手机号码不一致，通过手机号码搜索
        :return:
        '''

        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # time.sleep(3)
        # GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text('13800138000')
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("给个红包1")
        time.sleep(1)
        lcontact.click_text("给个红包1")
        time.sleep(1)
        lcontact.is_text_present("给个红包1")
        lcontact.is_text_present("13800138000")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0043(self):
        '''
      测试+86的手机号码，通过名称搜索
        :return:
        '''

        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xika")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("861 3410 5596 55")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0044(self):
        '''
      测试+86的手机号码，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+8613410559655")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+8613410559655")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0045(self):
        '''
      测试+86的手机号码，通过+搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+8613410559655")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0046(self):
        '''
      测试+86的手机号码，通过+86搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+86")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+8613410559655")
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0047(self):
        '''
      测试+86的手机号码，通过区号和手机号码前几个字符一起搜索（+8613512345123，搜索输入613等）
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("613")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+8613410559655")
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0048(self):
        '''
      测试+86的手机号码，通过输入前10位手机号码进行匹配搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("1341055965")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+8613410559655")
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0049(self):
        '''
        测试+86的手机号码，通过输入11位手机号码进行全匹配搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410559655")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+86 134 1055 9655")
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0050(self):
        '''
        测试+852的手机号码，通过名称搜索
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xiaowen")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xiaowen")
        time.sleep(1)
        lcontact.click_text("xiaowen")
        time.sleep(1)
        lcontact.is_text_present("xiaowen")
        lcontact.is_text_present("+852 134 1055 9644")
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0051(self):
        '''
        测试+852的手机号码，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410559644")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_text("xiaowen")
        time.sleep(1)
        lcontact.is_text_present("xiaowen")
        lcontact.is_text_present("+852 134 1055 9644")
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0052(self):
        '''
        测试+852的手机号码，通过+搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_text("xiaowen")
        time.sleep(1)
        lcontact.is_text_present("xiaowen")
        lcontact.is_text_present("+852 134 1055 9644")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0053(self):
        '''
        测试+852的手机号码，通过+852搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+852")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_text("xiaowen")
        time.sleep(1)
        lcontact.is_text_present("xiaowen")
        lcontact.is_text_present("+852 134 1055 9644")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0054(self):
        '''
        测试+852的手机号码，通过521搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("521")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_text("xiaowen")
        time.sleep(1)
        lcontact.is_text_present("xiaowen")
        lcontact.is_text_present("+852 134 1055 9644")
        lcontact.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0055(self):
        '''
        测试+852的手机号码，通过输入前7位手机号码进行匹配搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("1341055")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_back_by_android(1)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0056(self):
        '''
        测试+852的手机号码，通过输入前8位手机号码进行匹配搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410559")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_back_by_android(1)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0057(self):
        '''
        测试搜索内地固话，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("075528233375")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="wa ss")
        time.sleep(1)
        lcontact.click_back_by_android(1)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0058(self):
        '''
        测试搜索香港固话，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("67656003")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="香港大佬")
        lcontact.click_back_by_android(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0059(self):
        '''
        测试断网情况下，是否能读取本地联系人和搜索
        :return:
        '''
        lcontact = localContactPage()
        lcontact.set_network_status(0)
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410559")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_back_by_android(1)
        time.sleep(1)
        lcontact.set_network_status(6)

    @staticmethod
    def tearDown_test_contacts_chenjixiang_0059():
        # 初始化,恢复app到默认状态
        lcontact = localContactPage()
        lcontact.set_network_status(6)
        lcontact.click_back_by_android(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0060(self):
        '''
        测试通过名称搜索无号码的联系人
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("wushoujihao")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="无手机号")
        time.sleep(1)
        lcontact.click_back_by_android(1)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0061(self):
        '''
        测试搜索一个超长姓名和号码的联系人，搜索结果列表显示超长使用…
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("aaaaaaaaaaaaaaaaaaaa")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present('aaaaaaaaaaaaaaaaaaaa...')
        lcontact.check_keyword_if_exist(text="13410559633")
        lcontact.click_back_by_android(1)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0063(self):
        '''
        测试已经被过滤掉空格的联系人，通过空格搜索
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(" ")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)==0)
        lcontact.click_back_by_android()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0064(self):
        '''
        测试已经被过滤掉空格的联系人，通过姓名搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("wass")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')
        lcontact.click_back_by_android()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0065(self):
        '''
        测试号码已经被过滤掉的字符进行搜索（中英文、特殊字符、空格）的联系人，通过被过滤掉的字符进行搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("?")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)==0)
        lcontact.page_should_contain_text('无搜索结果')
        time.sleep(2)
        lcontact.click_back_by_android()



    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0066(self):
        '''
        测试号码已经被过滤掉的字符进行搜索（中英文、特殊字符、空格）的联系人，通过手机号码进行搜索
        :return:
        '''
        lcontact = localContactPage()

        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("67656022")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0067(self):
        '''
        测试sim单卡有联系人情况下，开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''

        time.sleep(2)
        ContactsPage().open_me_page()
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=True)
        lcontact.click_back_by_android(times=2)

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>1)
        # els2 = lcontact.get_element_number(text='SIM_联系人')
        # self.assertTrue(len(els2) > 0)
        lcontact.click_back_by_android()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0068(self):
        '''
        测试sim单卡有联系人情况下，未开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''
        time.sleep(2)
        ContactsPage().open_me_page()
        time.sleep(1)
        me_page = MePage()
        # me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_contacts_name()
        time.sleep(1)
        self.assertTrue(len(els)>1)
        lcontact.click_back_by_android()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0069(self):
        '''
        测试sim单卡无联系人情况下，开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''
        time.sleep(2)
        ContactsPage().open_me_page()
        time.sleep(1)
        me_page = MePage()
        # me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=True)
        lcontact.click_back_by_android(times=2)

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        # GroupPage.page_up()
        # time.sleep(1)
        els = lcontact.get_contacts_name()
        time.sleep(1)
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0070(self):
        '''
        测试sim单卡无联系人情况下，未开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''
        time.sleep(2)
        ContactsPage().open_me_page()
        time.sleep(2)
        me_page = MePage()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        GroupPage.page_up()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_chenjixiang_0083(self):
        """测试点击联系人跳转到profile页"""
        GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        time.sleep(1)
        ContactsPage().select_contacts_by_name('大佬4')
        time.sleep(2)
        GroupPage.page_contain_element(locator='语音通话')
        GroupPage.page_contain_element(locator='视频通话')
        GroupPage.page_contain_element(locator='分享名片')
        GroupPage.click_share_button()
        GroupPage.click_back_by_android(times=2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0085(self):
        '''
        测试系统通讯录一个联系人拥有多个手机号码，手机号码都不一样的情况下，显示多条（不去重）
        :return:
        '''
        lcontact = localContactPage()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(2)
        #显示多条结果，姓名一样，头像、手机号码不一样
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)
        name1=lcontact.get_all_contacts_name()[0].text
        name2 = lcontact.get_all_contacts_name()[1].text
        self.assertEqual(name1,name2)
        time.sleep(1)
        number1 = lcontact.get_all_contacts_number()[0].text
        number2 = lcontact.get_all_contacts_number()[1].text
        self.assertNotEqual(number1, number2)
        time.sleep(1)
        # 联系人头像是否一样无法判断
        # head1=lcontact.get_all_contacts_head()[0]
        # head2 = lcontact.get_all_contacts_head()[1]
        # self.assertNotEqual(head1,head2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0086(self):
        '''
        测试系统通讯录存在多个联系人，手机号码一样
        :return:
        '''
        # 添加手机联系人
        time.sleep(2)
        # 添加联系人
        ContactsPage().click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('13410669616')
        els = localContactPage().get_element_number()
        if len(els) > 1:
            contact_search.click_back()
        else:
            contact_search.click_back()
            ContactsPage().click_add()
            creat_contact = CreateContactPage()
            creat_contact.click_input_name()
            creat_contact.input_name('xili')
            creat_contact.click_input_number()
            creat_contact.input_number('13410669616')
            creat_contact.click_save()
            time.sleep(2)
            ContactDetailsPage().click_back()
            time.sleep(2)
        lcontact = localContactPage()
        # GroupPage = GroupListPage()
        # GroupPage.open_contacts_page()
        time.sleep(2)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669616")
        lcontact.hide_keyboard()
        time.sleep(2)
        #显示多条结果，姓名不一样，头像、手机号码一样
        els = lcontact.get_element_number()
        self.assertTrue(len(els) == 2)
        name1=lcontact.get_all_contacts_name()[0].text
        name2 = lcontact.get_all_contacts_name()[1].text
        self.assertNotEqual(name1,name2)
        time.sleep(1)
        number1 = lcontact.get_all_contacts_number()[0].text
        number2 = lcontact.get_all_contacts_number()[1].text
        self.assertEqual(number1, number2)
        time.sleep(1)
        # 联系人头像是否一样无法判断
        # head1=lcontact.get_all_contacts_head()[0]
        # head2 = lcontact.get_all_contacts_head()[1]
        # self.assertEqual(head1,head2)


class ContactsLocalhigh(TestCase):
    """
    模块：联系-本地联系人
    文件位置：全量/115全量测试用例-联系(1322).xlsx--高等级用例(优先编写)
    表格：通讯录-本地通讯录
    author: 余梦思
    """
    #
    # @classmethod
    # def setUpClass(cls):
    #     # 创建联系人
    #     fail_time = 0
    #     import dataproviders
    #
    #     while fail_time < 3:
    #         try:
    #             # 获取需要导入的联系人数据
    #             required_contacts = dataproviders.get_preset_contacts()
    #
    #             # 连接手机
    #             Preconditions.connect_mobile('Android-移动')
    #             Preconditions.make_already_in_message_page()
    #             current_mobile().hide_keyboard_if_display()
    #             conts = ContactsPage()
    #             conts.open_contacts_page()
    #             # 导入数据
    #             for name, number in required_contacts:
    #                 # Preconditions.create_contacts_if_not_exits(name, number)
    #                 Preconditions.create_contacts_if_not_exits(name, number)
    #
    #             # # 推送resource文件到手机
    #             # dataproviders.push_resource_dir_to_mobile_sdcard(Preconditions.connect_mobile('Android-移动'))
    #             return
    #         except:
    #             fail_time += 1
    #             import traceback
    #             msg = traceback.format_exc()
    #             print(msg)

    def default_setUp(self):
        """确保每个用例执行前在通讯录页面"""
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0123(self):
        """测试本地系统通讯录联系人，有姓名，头像，无号码，profile页是否正常"""
        #返回桌面,添加SIM卡联系人:无手机号
        contact = ContactsPage()
        Preconditions.background_app()
        time.sleep(1)
        contact.click_text('拨号')
        time.sleep(2)
        contact.click_text('联系人')
        time.sleep(1)
        contact.click_creat_contacts()
        time.sleep(1)
        contact.click_text('姓名')
        text='无手机号'
        contact.input_contact_text(text)
        contact.click_sure_SIM()
        time.sleep(2)
        #激活App
        Preconditions.activate_app()
        if contact.is_text_present('SIM卡联系人'):
            contact.click_text('显示')
        #判断无手机号联系人的个人详情页
        contact.select_contacts_by_name(text)
        contant_detail=ContactDetailsPage()
        contant_detail.is_exists_contacts_name()
        contant_detail.is_exists_contacts_image()
        contant_detail.page_should_contain_text('暂无号码')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0123(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().select_contacts_by_name('无手机号')
        time.sleep(2)
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        contant_detail.hide_keyboard()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0130(self):
        """测试表单字段，姓名非空校验"""
        ContactsPage().click_add()
        time.sleep(1)
        CreateContactPage().click_input_number()
        CreateContactPage().page_should_contain_text('姓名不能为空，请输入')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0137(self):
        """测试表单字段，手机号非空校验"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.click_input_name()
        creat_contact.page_should_contain_text('电话不能为空，请输入')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0138(self):
        """测试表单字段，手机号码长度校验，小于3个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('12')
        creat_contact.click_save()
        creat_contact.page_should_contain_text('号码输入有误，请重新输入')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0140(self):
        """测试表单字段，手机号码长度边界值校验，3个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('和飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0140(self):
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        contant_detail.hide_keyboard()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0147(self):
        """测试表单字段，公司边界值校验，输入1个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.click_input_company()
        creat_contact.input_company('a')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('和飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0147(self):
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        contant_detail.hide_keyboard()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0154(self):
        """测试表单字段，职位边界值校验，输入1个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.hide_keyboard()
        creat_contact.click_input_position()
        creat_contact.input_position('a')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('和飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0154(self):
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        contant_detail.hide_keyboard()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0161(self):
        """测试表单字段，邮箱边界值校验，输入1个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.hide_keyboard()
        creat_contact.click_input_email()
        creat_contact.input_email_address('a')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('和飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0161(self):
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        contant_detail.hide_keyboard()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0166(self):
        """测试和飞信新建联系人，名称和本地通讯录联系人一样，手机号码不一样"""
        # old_number=ContactsPage().get_all_phone_number()
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        input_name='大佬1'
        creat_contact.input_name(input_name)
        creat_contact.click_input_number()
        input_number='12345678901'
        creat_contact.input_number(input_number)
        creat_contact.click_save()
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.page_should_contain_text('和飞信电话')
        time.sleep(1)
        contact_name1=contact_detail.get_people_name()
        contact_number1=contact_detail.get_people_number()
        time.sleep(1)
        #原本的大佬1
        contact_detail.click_back_icon()
        time.sleep(1)
        ContactsPage().select_contacts_by_number('13800138005')
        time.sleep(2)
        contact_name2 = contact_detail.get_people_name()
        contact_number2 = contact_detail.get_people_number()
        #判断新增名称一样,号码与头像不一样
        time.sleep(1)
        self.assertEqual(contact_name1,contact_name2)
        self.assertNotEqual(contact_number1, contact_number2)

    def tearDown_test_contacts_chenjixiang_0166(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        contact = ContactsPage()
        if contact.is_exit_element_by_text_swipe('12345678901'):
            contact.select_contacts_by_number('12345678901')
            contant_detail = ContactDetailsPage()
            contant_detail.click_edit_contact()
            time.sleep(2)
            contant_detail.hide_keyboard()
            contant_detail.change_delete_number()
            contant_detail.click_sure_delete()
        else:
            pass

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0175(self):
        """测试页面信息展示，名称正常长度显示"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        contact_name=cdp.get_people_name()
        self.assertEqual(contact_name,'大佬1')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0177(self):
        """测试页面信息展示，手机号码正常长度显示"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        contact_name=cdp.get_people_number()
        self.assertEqual(contact_name,'13800138005')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0179(self):
        """测试页面信息展示，未上传头像"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.page_should_contain_element_first_letter()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0180(self):
        """测试页面信息展示，已上传头像"""
        ContactsPage().select_contacts_by_name('测试号码1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.page_contain_contacts_avatar()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0181(self):
        """测试点击联系人头像，未上传头像"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.click_avatar()
        cdp.is_exists_big_avatar()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0182(self):
        """测试点击联系人头像，已上传头像"""
        ContactsPage().select_contacts_by_name('测试号码1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.click_avatar()
        cdp.is_exists_big_avatar()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0193(self):
        """测试编辑联系人信息，正常"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #编辑手机号码
        creat_contact=CreateContactPage()
        creat_contact.click_input_number()
        creat_contact.change_mobile_number(text='13800138789')
        contact_number=creat_contact.get_contant_number()
        creat_contact.click_save()
        time.sleep(2)
        #查看改变后的联系人
        cdp.click_back_icon()
        ContactsPage().select_contacts_by_name('大佬1')
        contact_number2=cdp.get_people_number()
        self.assertNotEqual(contact_number, contact_number2)

    def tearDown_test_contacts_chenjixiang_0193(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        time.sleep(2)
        ContactsPage().select_contacts_by_name('大佬1')
        #恢复联系人电话号码
        number=ContactDetailsPage().get_people_number()
        if number == '13800138005':
            ContactDetailsPage().click_back_icon()
        else:
            ContactDetailsPage().click_edit_contact()
            creat_contact = CreateContactPage()
            creat_contact.click_input_number()
            creat_contact.change_mobile_number(text='13800138005')
            creat_contact.click_save()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0194(self):
        """测试表单字段，姓名非空校验"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 姓名为空,保存按钮不可点击
        creat_contact = CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('')
        creat_contact.is_save_icon_is_clickable()
        # 姓名为必填项
        creat_contact.click_input_number()
        creat_contact.page_should_contain_text('姓名不能为空，请输入')
        time.sleep(2)
        creat_contact.click_back()


    # @tags('ALL', 'CONTACTS', 'CMCC')
    # def test_contacts_chenjixiang_00001(self):
    #     ContactsPage().select_contacts_by_name('大佬1')
    #     time.sleep(2)
    #     ContactDetailsPage().click_message_icon()
    #     chat=ChatWindowPage()
    #     chat.click_msg_input_box()
    #     chat.input_message_text('asasa')
    #     chat.click_send_button()
    #     #更改手机时间,使最后一条消息发送时间超过10分钟
    #     Preconditions.background_app()
    #     time.sleep(3)
    #     chat.click_text('设置')
    #     chat.page_up()
    #     chat.click_text('系统')
    #     time.sleep(3)
    #     chat.click_text('日期和时间')
    #     time.sleep(2)
    #     chat.swich_automatic_time(flag=False)
    #     chat.click_date_in_setting()
    #     time.sleep(1)
    #     chat.swipe_month("2021", 0)
    #     time.sleep(1)
    #     chat.swipe_month("9", 1)
    #     time.sleep(1)
    #     chat.swipe_month("26", 2)
    #

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0201(self):
        """个人profile页,编辑联系人-手机号码不为空"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #手机号为空,保存按钮不可点击
        creat_contact=CreateContactPage()
        creat_contact.click_input_number()
        creat_contact.input_number('')
        creat_contact.is_save_icon_is_clickable()
        #手机为必填项
        creat_contact.click_input_name()
        creat_contact.page_should_contain_text('电话不能为空，请输入')
        time.sleep(2)
        creat_contact.click_back()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0206(self):
        """个人profile页,编辑联系人-公司为非必填项"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #姓名为空,保存按钮不可点击
        creat_contact=CreateContactPage()
        creat_contact.click_input_number()
        creat_contact.change_mobile_number(text='#')
        creat_contact.page_should_contain_text('号码输入有误，请重新输入')
        time.sleep(2)
        creat_contact.click_back()

    @tags('ALL', 'CONTACTS', 'CMCC',)
    def test_contacts_chenjixiang_0209(self):
        """个人profile页,编辑联系人-公司为非必填项"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #姓名为空,保存按钮不可点击
        creat_contact=CreateContactPage()
        creat_contact.click_input_company()
        time.sleep(2)
        creat_contact.click_input_name()
        creat_contact.is_save_icon_is_clickable()
        time.sleep(2)
        creat_contact.click_save()
        ContactDetailsPage().is_on_this_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0214(self):
        """个人profile页,编辑联系人-公司为非必填项"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #姓名为空,保存按钮不可点击
        creat_contact=CreateContactPage()
        creat_contact.click_input_company()
        creat_contact.input_company('#$sda我的123')
        time.sleep(2)
        creat_contact.is_save_icon_is_clickable()
        creat_contact.click_save()
        ContactDetailsPage().is_on_this_page()

    def test_contacts_chenjixiang_0228(self):
        """个人profile页,编辑联系人-公司为非必填项"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #姓名为空,保存按钮不可点击
        creat_contact=CreateContactPage()
        creat_contact.hide_keyboard()
        creat_contact.click_input_email()
        creat_contact.input_email_address('#$sda我的123')
        time.sleep(2)
        creat_contact.is_save_icon_is_clickable()
        creat_contact.click_save()
        ContactDetailsPage().is_on_this_page()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0230(self):
        """个人profile页,编辑联系人-删除联系人"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        name=cdp.get_people_name()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        cdp.hide_keyboard()
        cdp.page_up()
        cdp.change_delete_number()
        cdp.click_sure_delete()
        time.sleep(2)
        ContactsPage().is_contacts_exist(name)

    def tearDown_test_contacts_chenjixiang_0230(self):
        #删除联系人后添加该联系人
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().click_add()
        time.sleep(2)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('大佬1')
        creat_contact.click_input_number()
        creat_contact.input_number('13800138005')
        creat_contact.click_save()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0237(self):
        """测试分享名片，跳转到联系人选择器"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_share_card_icon()
        time.sleep(2)
        scp=SelectContactsPage()
        scp.is_on_this_page()
        scp.page_should_contain_text('搜索或输入手机号')
        scp.page_should_contain_text('选择一个群')
        scp.page_should_contain_text('选择团队联系人')
        scp.page_should_contain_text('选择手机联系人')
        if scp.check_if_element_exist(text='联系人姓名'):
            scp.page_should_contain_text('最近聊天')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0238(self):
        """测试和飞信电话，登录本网卡显示，可拨打成功"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_voice_call_icon()
        time.sleep(1)
        if cdp.is_text_present('暂不开启'):
            cdp.click_text('暂不开启')
        time.sleep(1)
        cdp.click_end_call()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0242(self):
        """测试星标点击"""
        ContactsPage().select_contacts_by_name('大佬1')
        glp = GroupListPage()
        time.sleep(2)
        glp.click_star_icon()
        glp.page_should_contain_text('已成功添加为星标联系人')

    def tearDown_test_contacts_chenjixiang_0242(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().select_contacts_by_name('大佬1')
        glp = GroupListPage()
        time.sleep(2)
        glp.click_star_icon()
        if glp.is_text_present('已取消添加为星标联系人'):
            pass
        else:
            glp.click_star_icon()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0243(self):
        """测试取消星标"""
        #添加联系人是星标联系人
        ContactsPage().select_contacts_by_name('大佬1')
        glp = GroupListPage()
        time.sleep(2)
        glp.click_star_icon()
        glp.page_should_contain_text('已成功添加为星标联系人')
        #取消添加星标联系人
        glp.click_star_icon()
        glp.page_should_contain_text('已取消添加为星标联系人')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0246(self):
        """测试消息，点击消息，跳转到对话框"""
        #添加联系人是星标联系人
        ContactsPage().select_contacts_by_name('大佬1')
        glp = GroupListPage()
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            #如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
        SingleChatPage().is_on_this_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0247(self):
        """测试电话，点击后调用系统通话，拨打电话"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.click_call_icon()
        if cdp.is_text_present('始终允许'):
            cdp.click_text('始终允许')
        time.sleep(2)
        cdp.cancel_call()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0248(self):
        """测试语音通话，点击后弹出语音通话框"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.click_voice_call_icon()
        if cdp.is_text_present('始终允许'):
            cdp.click_text('始终允许')
        if cdp.is_text_present('暂不开启'):
            time.sleep(2)
            cdp.click_text('暂不开启')
        time.sleep(2)
        cdp.click_end_call()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0264(self):
        """测试和通讯录联系人profile，没有快捷方式功能"""
        contact=ContactsPage()
        contact.select_group_by_name('ateam7272')
        contact.select_group_contact_by_name('alice')
        ContactDetailsPage().page_should_not_contain_text('添加桌面快捷方式')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0265(self):
        """测试RCS用户，已设置和飞信头像时，添加桌面快捷方式的显示效果"""
        ContactsPage().select_contacts_by_name('大佬1')
        contact_detail=ContactDetailsPage()
        contact_detail.click_add_desktop_shortcut()
        time.sleep(2)
        contact_detail.click_I_know()
        time.sleep(1)
        if contact_detail.is_text_present('添加到主屏幕'):
            contact_detail.click_sure_add_desktop_shortcut()
        time.sleep(2)
        Preconditions.background_app()
        time.sleep(2)
        contact_detail.is_element_present_on_desktop('大佬1')
        contact_detail.click_text('大佬1')
        time.sleep(2)
        contact_detail.page_should_contain_text('添加桌面快捷方式')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0268(self):
        """测试非RCS用户，已设置和飞信头像时，添加桌面快捷方式的显示效果"""
        ContactsPage().select_contacts_by_name('测试号码')
        contact_detail=ContactDetailsPage()
        #添加桌面快捷方式
        contact_detail.click_add_desktop_shortcut()
        time.sleep(2)
        contact_detail.click_I_know()
        time.sleep(1)
        if contact_detail.is_text_present('添加到主屏幕'):
            contact_detail.click_sure_add_desktop_shortcut()
        time.sleep(2)
        Preconditions.background_app()
        time.sleep(2)
        contact_detail.is_element_present_on_desktop('测试号码')
        #快捷方式进入app
        contact_detail.click_text('测试号码')
        time.sleep(2)
        contact_detail.page_should_contain_text('添加桌面快捷方式')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0270(self):
        """测试点击快捷方式跳转，进入profile页后进行功能操作，和页面返回跳转等"""
        #从快捷方式进入页面
        contact=ContactsPage()
        time.sleep(2)
        Preconditions.background_app()
        contact.is_element_present_on_desktop('测试号码')
        contact.click_text('测试号码')
        #个人详情页
        time.sleep(3)
        glp=GroupListPage()
        glp.page_should_contain_text('添加桌面快捷方式')
        #星标
        glp.click_star_icon()
        glp.page_should_contain_text('已成功添加为星标联系人')
        time.sleep(2)
        glp.click_star_icon()
        #点击编辑
        ContactDetailsPage().click_edit_contact()
        time.sleep(2)
        creat_contact=CreateContactPage()
        creat_contact.hide_keyboard()
        if creat_contact.get_text_of_box() == None:
            creat_contact.click_input_company()
            creat_contact.hide_keyboard()
            creat_contact.input_company('sds')
            creat_contact.click_save()
        else:
            creat_contact.click_back()
        #点击返回
        time.sleep(2)
        creat_contact.click_back()
        MessagePage().is_on_this_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0277(self):
        """测试客户端退出登陆后，点击快捷方式"""
        #退出客户端
        contact=ContactsPage()
        time.sleep(2)
        contact.open_me_page()
        me=MePage()
        me.page_up()
        me.click_setting_menu()
        me.page_down()
        me.click_text('退出')
        time.sleep(1)
        me.click_sure_drop()
        time.sleep(4)
        #从快捷方式进入
        Preconditions.background_app()
        contact.is_element_present_on_desktop('测试号码')
        contact.click_text('测试号码')
        time.sleep(5)
        #检查是否在登录界面
        OneKeyLoginPage().is_on_this_page()

    def tearDown_test_contacts_chenjixiang_0277(self):
        Preconditions.login_by_one_key_login()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0250(self):
        """测试视频通话，点击后弹出视频通话框"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.click_video_call_icon()
        if cdp.is_text_present('始终允许'):
            cdp.click_text('始终允许')
        if cdp.is_text_present('暂不开启'):
            time.sleep(1)
            cdp.click_text('暂不开启')
        time.sleep(2)
        cdp.end_video_call()

    def setUp_test_contacts_chenjixiang_0253(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=True)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0253(self):
        """测试sim联系人profile页显示是否正常"""
        #确保有SIM卡联系人
        GroupListPage().open_contacts_page()
        contact = ContactsPage()
        if ContactsPage().is_page_contain_element('sim标志'):
            time.sleep(2)
        else:
            contact.add_SIM_contacts()
            #激活App
            Preconditions.activate_app()
            time.sleep(2)
            if contact.is_text_present('SIM卡联系人'):
                contact.click_text('显示')
        #查看SIM卡联系人的个人详情页
        contact.click_SIM_identification()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('来自SIM卡联系人')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0259(self):
        """测试本地联系人profile页，分享名片下方新增添加快捷方式"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.page_should_contain_text('添加桌面快捷方式')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0283(self):
        """测试创建快捷方式后，删除联系人"""
        contact=ContactsPage()
        contact.select_contacts_by_name('测试号码')
        time.sleep(1)
        #删除联系人
        ContactDetailsPage().click_edit_contact()
        time.sleep(2)
        edit_contact=EditContactPage()
        edit_contact.hide_keyboard()
        edit_contact.click_delete_contact()
        time.sleep(1)
        edit_contact.click_sure_delete()
        time.sleep(2)
        #从快捷方式进入
        Preconditions.background_app()
        contact.is_element_present_on_desktop('测试号码')
        contact.click_text('测试号码')
        time.sleep(2)
        ContactsPage().page_should_contain_text('联系')

    def tearDown_test_contacts_chenjixiang_0283(self):
        #删除联系人后添加该联系人
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_contacts_exist('测试号码'):
            pass
        else:
            ContactsPage().click_add()
            time.sleep(2)
            CreateContactPage().create_contact('测试号码','14775970982')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0294(self):
        """测试sim联系人profile页显示是否正常"""
        #确保有SIM卡联系人
        contact = ContactsPage()
        if ContactsPage().is_page_contain_element('sim标志'):
            time.sleep(2)
        else:
            contact.add_SIM_contacts()
            #激活App
            Preconditions.activate_app()
            time.sleep(2)
            if contact.is_text_present('SIM卡联系人'):
                contact.click_text('显示')
        #查看SIM卡联系人的个人详情页
        contact.click_SIM_identification()
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.page_should_contain_text('来自SIM卡联系人')
        name=contact_detail.get_people_name()
        #添加桌面快捷方式
        contact_detail.click_add_desktop_shortcut()
        time.sleep(2)
        contact_detail.click_I_know()
        time.sleep(1)
        if contact_detail.is_text_present('添加到主屏幕'):
            contact_detail.click_sure_add_desktop_shortcut()
        time.sleep(2)
        Preconditions.background_app()
        time.sleep(2)
        contact_detail.is_element_present_on_desktop(name)
        #快捷方式进入app
        contact_detail.click_text(name)
        time.sleep(2)
        contact_detail.page_should_contain_text('添加桌面快捷方式')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0308(self):
        """号码过滤-空格过滤：和飞信通讯录联系人编辑页过滤系统通讯录联系人手机号码中间的空格"""
        time.sleep(2)
        #确保有SIM卡联系人
        contact = ContactsPage()
        if ContactsPage().is_contacts_exist('系统1'):
            time.sleep(2)
        else:
            contact.add_system_contacts()
            #激活App
            Preconditions.activate_app()
            time.sleep(2)
            if contact.is_text_present('SIM卡联系人'):
                contact.click_text('显示')
        #查看SIM卡联系人的电话号码不显示空格
        contact.select_contacts_by_name('系统1')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.click_edit_contact()
        time.sleep(2)
        number =CreateContactPage().get_text_of_box(locator='输入号码')
        self.assertEqual(number,'13813813801')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0315(self):
        """号码过滤-中英文、特殊符号：和飞信通讯录个人profile页过滤系统通讯录联系人手机号码中间的中英文、特殊符号（不包含+）"""
        contact = ContactsPage()
        # 创建sim联系人手机号含有英文等
        local_name = '系统2'
        local_number = '138aaa;1380'
        if ContactsPage().is_contacts_exist(local_name):
            time.sleep(2)
        else:
            contact.add_system_contacts(name=local_name, number=local_number)
            # 激活App
            Preconditions.activate_app()
            time.sleep(2)
            if contact.is_text_present('SIM卡联系人'):
                contact.click_text('显示')
        # 进入该联系人个人详情页查看
        contact.select_contacts_by_name(local_name)
        contact_detail = ContactDetailsPage()
        contact_number = contact_detail.get_people_number()
        self.assertNotEqual(local_number, contact_number)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0319(self):
        """号码过滤-中英文、特殊符号：和飞信通讯录个人profile页过滤系统通讯录联系人手机号码所有的中英文、特殊符号（不包含+"""
        contact = ContactsPage()
        # 创建sim联系人手机号含有英文等
        local_name = '系统3'
        local_number = 'a138aa;138a'
        if ContactsPage().is_contacts_exist(local_name):
            time.sleep(2)
        else:
            contact.add_system_contacts(name=local_name, number=local_number)
            # 激活App
            Preconditions.activate_app()
            time.sleep(2)
            if contact.is_text_present('SIM卡联系人'):
                contact.click_text('显示')
        # 进入该联系人个人详情页查看
        contact.select_contacts_by_name(local_name)
        contact_detail = ContactDetailsPage()
        contact_number = contact_detail.get_people_number()
        self.assertNotEqual(local_number, contact_number)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0325(self):
        """号码过滤：大陆号码+号过滤:和飞信通讯录个人frofile页过滤系统通讯录联系人大陆号码后面的+号"""
        contact = ContactsPage()
        # 创建sim联系人手机号含有英文等
        local_name = '系统4'
        local_number = '13801380+++'
        if ContactsPage().is_contacts_exist(local_name):
            time.sleep(2)
        else:
            contact.add_system_contacts(name=local_name, number=local_number)
            # 激活App
            Preconditions.activate_app()
            time.sleep(2)
            if contact.is_text_present('SIM卡联系人'):
                contact.click_text('显示')
        # 进入该联系人个人详情页查看
        contact.select_contacts_by_name(local_name)
        contact_detail = ContactDetailsPage()
        contact_number = contact_detail.get_people_number()
        self.assertNotEqual(local_number, contact_number)


if __name__=="__main__":
    unittest.main()
