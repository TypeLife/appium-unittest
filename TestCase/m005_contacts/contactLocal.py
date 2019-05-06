import unittest
import uuid
import time
import threading
from preconditions.BasePreconditions import LoginPreconditions
from library.core.common.simcardtype import CardType
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
            Preconditions.make_already_in_message_page(reset_required=False)
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
            Preconditions.make_already_in_message_page(reset_required=False)
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
    '''
    通讯录测试记录-陈计祥
    '''
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


    def default_setUp(self):
        """确保每个用例运行前在通讯录页面"""
        # Preconditions.connect_mobile('Android-移动')
        # current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0001(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入数字模糊查询（只搜索一条记录）
        author:darcy

        :return:
        '''
        lcontact=localContactPage()
        lcontact.click_search_box()
        lcontact.input_search_text(text='138005')
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

    # @tags('ALL', 'CONTACTS', 'CMCC')
    # def test_contacts_chenjixiang_0003(self):
    #     '''
    #     搜索输入框校验，通过手机号码搜索，输入手机号码全匹配查询
    #     auther:darcy
    #     :return:
    #     '''
    #     lcontact = localContactPage()
    #     lcontact.click_search_box()
    #     time.sleep(1)
    #     lcontact.input_search_text(text='13800138001')
    #     time.sleep(1)
    #     lcontact.hide_keyboard()
    #     time.sleep(3)
    #     lcontact.page_contain_element()
    #     lcontact.page_contain_element(text='联系人电话')
    #     lcontact.page_contain_element(text='联系人名字')
    #
    # @tags('ALL', 'CONTACTS', 'CMCC')
    # def test_contacts_chenjixiang_0004(self):
    #     '''
    #     搜索输入框校验，通过名称(中文)搜索(多条记录)
    #     auther:darcy
    #     :return:
    #     '''
    #     lcontact = localContactPage()
    #     lcontact.click_search_box()
    #     time.sleep(1)
    #     lcontact.input_search_text(text='给个红包')
    #     time.sleep(1)
    #     lcontact.hide_keyboard()
    #     time.sleep(3)
    #     lcontact.page_contain_element()
    #     lcontact.page_contain_element(text='联系人电话')
    #     lcontact.page_contain_element(text='联系人名字')
    #
    # @tags('ALL', 'CONTACTS', 'CMCC')
    # def test_contacts_chenjixiang_0005(self):
    #     '''
    #     搜索输入框校验，通过名称(英文)搜索(多条记录)
    #     auther:darcy
    #     :return:
    #     '''
    #     lcontact = localContactPage()
    #     lcontact.click_search_box()
    #     time.sleep(1)
    #     lcontact.input_search_text(text='ABC')
    #     time.sleep(1)
    #     lcontact.hide_keyboard()
    #     time.sleep(3)
    #     lcontact.page_contain_element()
    #     lcontact.page_contain_element(text='联系人电话')
    #     lcontact.page_contain_element(text='联系人名字')
    #



    @staticmethod
    def setUp_test_contacts_chenjixiang_0019():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        lcontact.is_text_present("无该本地联系人")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0020():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
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
        lcontact.input_search_text("xili")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0021():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        lcontact.is_text_present("无该本地联系人")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0022():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        lcontact.input_search_text("ximi")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0005():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0005(self):
        '''
        搜索输入框校验，通过名称搜索，输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='1-a')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0006():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0006(self):
        '''
        搜索输入框校验，通过名称搜索，输入名称全匹配搜索（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='1-a子')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0004():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0004(self):
        '''
        搜索输入框校验，通过名称（中文）搜索，输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='大佬')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)


    @staticmethod
    def setUp_test_contacts_chenjixiang_0007():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0007(self):
        '''
        测试空格+文本进行搜索
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='wa s')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        lcontact.page_contain_element()
        lcontact.page_contain_element(text='联系人电话')
        lcontact.page_contain_element(text='联系人名字')


    @staticmethod
    def setUp_test_contacts_chenjixiang_0008():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0008(self):
        '''
        搜索输入框校验，通过名称搜索（英文），输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(text='wa')
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 1)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0010():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0010(self):
        '''
        测试搜索输入框输入超长字符
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        name='aa'*100
        lcontact.input_search_text(text=name)
        time.sleep(1)
        lcontact.hide_keyboard()


    @staticmethod
    def setUp_test_contacts_chenjixiang_0012():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0012(self):
        '''
        测试搜索输入框的X按钮是否可以清空内容
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        name = 'aa' * 100
        lcontact.input_search_text(text=name)
        lcontact.click_delete_button()
        lcontact.is_text_present("搜索")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0014():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0014(self):
        '''
        搜索一个不存在本地的正常的11位号码
        auther:darcy
        :return:

        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410889633")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无该本地联系人")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0015():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0015(self):
        '''
        搜索一个不存在本地的正常的11位号码
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
        lcontact.is_text_present("无该本地联系人")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0016():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(3)
        me_page = MePage()
        me_page.open_me_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0017():
        Preconditions.connect_mobile('Android-移动')

        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
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
        lcontact.is_text_present("无该本地联系人")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0018():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0023():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        lcontact.input_search_text("xiaomi")
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(3)
        time.sleep(1)
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("无该本地联系人")


    @staticmethod
    def setUp_test_contacts_chenjixiang_0024():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('联系人管理')
        lcontact = localContactPage()
        lcontact.swich_sim_contact(flag=False)
        lcontact.click_back_by_android(times=2)

    @tags('ALL', 'CONTACTS', 'CMCC')
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
        lcontact.is_text_present("无该本地联系人")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0030():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0030(self):
        '''
       测试搜索结果点击后跳转到profile页面
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0031():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0031(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码不一致的情况，通过名称搜索
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(2)
        els=lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android(times=1)
        lcontact.is_text_present("13410669632")
        lcontact.is_text_present("13410669625")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0032():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0032(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码不一致的情况，通过手机号码搜索
        auther:darcy
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669632")
        lcontact.hide_keyboard()
        time.sleep(2)
        lcontact.is_text_present("xili")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0033():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0033(self):
        '''
       测试系统通讯录联系人拥有多个手机号码，手机号码一致的情况，通过名称搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669616")
        lcontact.hide_keyboard()
        time.sleep(2)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0035():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0035(self):
        '''
       测试系统通讯录存在多个联系人，名称相同，手机号码不一致，通过名称搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        time.sleep(3)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(2)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.is_text_present("13410669632")
        lcontact.is_text_present("13410669625")
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0036():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0036(self):
        '''
       测试系统通讯录存在多个联系人，名称相同，手机号码不一致，通过手机号码搜索
        :return:
        '''

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669632")
        lcontact.hide_keyboard()
        time.sleep(2)
        lcontact.is_text_present("xili")
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.click_back_by_android()


    @staticmethod
    def setUp_test_contacts_chenjixiang_0039():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0039(self):
        '''
       测试系统通讯录存在多个联系人，名称不一致，手机号码相同，通过名称搜索
        :return:
        '''

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0040():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0040(self):
        '''
       测试系统通讯录存在多个联系人，名称不一致，手机号码相同，通过手机号码搜索
        :return:
        '''

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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


    @staticmethod
    def setUp_test_contacts_chenjixiang_0041():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0041(self):
        '''
       测试系统通讯录存在多个联系人，名称和手机号码不一致，通过名称搜索
        :return:
        '''

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("1-a")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("1-a")
        time.sleep(1)
        lcontact.click_text("1-a")
        time.sleep(1)
        lcontact.is_text_present("1-a")
        lcontact.is_text_present("6765 6004")
        lcontact.click_back_by_android(times=2)



    @staticmethod
    def setUp_test_contacts_chenjixiang_0042():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0042(self):
        '''
       测试系统通讯录存在多个联系人，名称和手机号码不一致，通过手机号码搜索
        :return:
        '''

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("67656004")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("1-a")
        time.sleep(1)
        lcontact.click_text("1-a")
        time.sleep(1)
        lcontact.is_text_present("1-a")
        lcontact.is_text_present("6765 6004")
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0043():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0043(self):
        '''
      测试+86的手机号码，通过名称搜索
        :return:
        '''

        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0044():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0044(self):
        '''
      测试+86的手机号码，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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
        lcontact.is_text_present("+86 134 1055 9655")
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0045():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0045(self):
        '''
      测试+86的手机号码，通过+搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+86 134 1055 9655")
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0046():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0046(self):
        '''
      测试+86的手机号码，通过+搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("+86")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+86 134 1055 9655")
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0047():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0047(self):
        '''
      测试+86的手机号码，通过区号和手机号码前几个字符一起搜索（+8613512345123，搜索输入613等）
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("613")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.is_text_present("xika")
        time.sleep(1)
        lcontact.click_text("xika")
        time.sleep(1)
        lcontact.is_text_present("xika")
        lcontact.is_text_present("+86 134 1055 9655")
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0048():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0048(self):
        '''
      测试+86的手机号码，通过输入前10位手机号码进行匹配搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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
        lcontact.is_text_present("+86 134 1055 9655")
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0049():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0049(self):
        '''
        测试+86的手机号码，通过输入11位手机号码进行全匹配搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0050():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0050(self):
        '''
        测试+852的手机号码，通过名称搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0051():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0051(self):
        '''
        测试+852的手机号码，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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


    @staticmethod
    def setUp_test_contacts_chenjixiang_0052():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0052(self):
        '''
        测试+852的手机号码，通过+搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0053():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0053(self):
        '''
        测试+852的手机号码，通过+852搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0054():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0054(self):
        '''
        测试+852的手机号码，通过521搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0055():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0055(self):
        '''
        测试+852的手机号码，通过输入前7位手机号码进行匹配搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("1341055")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_back_by_android(1)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0056():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0056(self):
        '''
        测试+852的手机号码，通过输入前8位手机号码进行匹配搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410559")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="xiaowen")
        time.sleep(1)
        lcontact.click_back_by_android(1)


    @staticmethod
    def setUp_test_contacts_chenjixiang_0057():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0057(self):
        '''
        测试搜索内地固话，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("075528233375")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="wa ss")
        time.sleep(1)
        lcontact.click_back_by_android(1)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0058():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0058(self):
        '''
        测试搜索香港固话，通过手机号码搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("67656003")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="香港大佬")
        lcontact.click_back_by_android(1)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0059():
        Preconditions.connect_mobile('Android-移动')
        lcontact = localContactPage()
        lcontact.set_network_status(0)
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0059(self):
        '''
        测试断网情况下，是否能读取本地联系人和搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
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

    @staticmethod
    def setUp_test_contacts_chenjixiang_0060():
        Preconditions.connect_mobile('Android-移动')
        lcontact = localContactPage()
        lcontact.set_network_status(0)
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0060(self):
        '''
        测试通过名称搜索无号码的联系人
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("wuhaoma")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="wuhaoma")
        time.sleep(1)
        lcontact.click_back_by_android(1)

    @staticmethod
    def tearDown_test_contacts_chenjixiang_0060():
        # 初始化,恢复app到默认状态
        lcontact = localContactPage()
        lcontact.set_network_status(6)
        lcontact.click_back_by_android(1)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0061():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0061(self):
        '''
        测试搜索一个超长姓名和号码的联系人，搜索结果列表显示超长使用…
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        lcontact.hide_keyboard()
        time.sleep(1)
        lcontact.check_keyword_if_exist(text="aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        lcontact.check_keyword_if_exist(text="13410559633")
        lcontact.click_back_by_android(1)


    @staticmethod
    def setUp_test_contacts_chenjixiang_0063():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0063(self):
        '''
        测试已经被过滤掉空格的联系人，通过空格搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text(" ")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)==0)
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0064():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0064(self):
        '''
        测试已经被过滤掉空格的联系人，通过姓名搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("wass")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()


    @staticmethod
    def setUp_test_contacts_chenjixiang_0065():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0065(self):
        '''
        测试号码已经被过滤掉的字符进行搜索（中英文、特殊字符、空格）的联系人，通过被过滤掉的字符进行搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("ss")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0066():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0066(self):
        '''
        测试号码已经被过滤掉的字符进行搜索（中英文、特殊字符、空格）的联系人，通过手机号码进行搜索
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("67656022")
        lcontact.hide_keyboard()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0067():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0067(self):
        '''
        测试sim单卡有联系人情况下，开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        els2 = lcontact.get_element_number(text='SIM_联系人')
        self.assertTrue(len(els2) > 0)
        lcontact.click_back_by_android()


    @staticmethod
    def setUp_test_contacts_chenjixiang_0068():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0068(self):
        '''
        测试sim单卡有联系人情况下，未开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        els = lcontact.get_element_number()
        self.assertTrue(len(els)==3)
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0069():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0069(self):
        '''
        测试sim单卡无联系人情况下，开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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
        GroupPage.page_up()
        time.sleep(1)
        els = lcontact.get_element_number()
        self.assertTrue(len(els)>0)
        lcontact.click_back_by_android()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0070():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0070(self):
        '''
        测试sim单卡无联系人情况下，未开启“显示sim卡联系人”，和飞信本地通讯录是否能读取到
        :return:
        '''
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
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



    @staticmethod
    def setUp_test_contacts_chenjixiang_0083():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_chenjixiang_0083(self):
        """测试点击联系人跳转到profile页"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        time.sleep(1)
        GroupPage.click_contact_element()
        time.sleep(1)
        GroupPage.page_contain_element(locator='语音通话')
        GroupPage.page_contain_element(locator='视频通话')
        GroupPage.page_contain_element(locator='分享名片')
        GroupPage.click_share_button()
        GroupPage.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_contacts_chenjixiang_0083():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()
        time.sleep(1)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_chenjixiang_0083(self):
        """测试点击联系人跳转到profile页"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        time.sleep(1)
        GroupPage.click_contact_element()
        time.sleep(1)
        GroupPage.page_contain_element(locator='语音通话')
        GroupPage.page_contain_element(locator='视频通话')
        GroupPage.page_contain_element(locator='分享名片')
        GroupPage.click_share_button()
        GroupPage.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_contacts_chenjixiang_0085():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0085(self):
        '''
        测试系统通讯录一个联系人拥有多个手机号码，手机号码都不一样的情况下，显示多条
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("xili")
        lcontact.hide_keyboard()
        time.sleep(2)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0086():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0086(self):
        '''
        测试系统通讯录存在多个联系人，手机号码一样
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("13410669616")
        lcontact.hide_keyboard()
        time.sleep(2)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0087():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0087(self):
        '''
        测试系统通讯录存在多个联系人，手机号码不一样
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("dalao")
        lcontact.hide_keyboard()
        time.sleep(2)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_contacts_chenjixiang_0088():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(3)
        preconditions.launch_app()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0088(self):
        '''
        测试单卡情况下，sim卡和本地联系人手机号码一样的情况
        :return:
        '''
        lcontact = localContactPage()
        GroupPage = GroupListPage()
        time.sleep(3)
        GroupPage.open_contacts_page()
        time.sleep(1)
        lcontact.click_search_box()
        time.sleep(1)
        lcontact.input_search_text("dalao")
        lcontact.hide_keyboard()
        time.sleep(2)
        els = lcontact.get_element_number()
        self.assertTrue(len(els) > 0)
        lcontact.click_back_by_android(times=2)

if __name__=="__main__":
    unittest.main()
