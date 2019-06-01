import random
import time
import unittest
import preconditions
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.EditContactPage import EditContactPage


class Preconditions(LoginPreconditions):
    """前置条件"""


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_contacts_chenjixiang_0083():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0083(self):
        """联系-选择一个联系人"""
        contacts = ContactsPage()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0083_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
            cdp.wait_for_page_load()
            cdp.click_back_icon()
            contacts = ContactsPage()
            time.sleep(1)
        else:
            name = names[0]
        contacts.is_exist_contracts_list()
        contacts.select_contacts_by_name(name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        self.assertTrue(cdp.is_on_this_page())


    @staticmethod
    def setUp_test_contacts_chenjixiang_0130():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0130(self):
        """联系-创建一个联系人-编辑-让姓名为空"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.click_input_name()
        ccp.click_input_number()
        self.assertTrue(ccp.is_toast_exist("姓名不能为空，请输入"))
        ccp.assert_save_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0137():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0137(self):
        """联系-创建一个联系人-编辑-让手机为空"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.click_input_name()
        ccp.input_name("test")
        time.sleep(1)
        ccp.click_input_number()
        time.sleep(1)
        ccp.click_input_name()
        self.assertTrue(ccp.is_toast_exist("手机号码不能为空，请输入"))
        ccp.assert_save_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0138():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0138(self):
        """联系-创建一个联系人-编辑-让手机位数小于3"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.click_input_name()
        ccp.input_name("test")
        time.sleep(1)
        ccp.click_input_number()
        ccp.input_number("13")
        time.sleep(1)
        ccp.click_input_name()
        self.assertTrue(ccp.is_toast_exist("号码输入有误，请重新输入"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0140():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0140(self):
        """联系-创建一个联系人-编辑-让手机位数为3"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0138_" + str(random.randint(100, 999))
        ccp.click_input_name()
        ccp.input_name(name)
        time.sleep(1)
        ccp.click_input_number()
        ccp.input_number("138")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0147():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0147(self):
        """联系-创建一个联系人-编辑-公司输入1个字符"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0147_" + str(random.randint(100, 999))
        ccp.input_name(name)
        number = "147752" + str(time.time())[-5:]
        ccp.input_number(number)
        ccp.hide_keyboard_if_display()
        ccp.input_company("a")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0154():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0154(self):
        """联系-创建一个联系人-编辑-职位输入1个字符"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0154_" + str(random.randint(100, 999))
        ccp.input_name(name)
        number = "147752" + str(time.time())[-5:]
        ccp.input_number(number)
        ccp.hide_keyboard_if_display()
        ccp.input_position("a")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0161():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0161(self):
        """联系-创建一个联系人-编辑-邮箱输入1个字符"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0161_" + str(random.randint(100, 999))
        ccp.input_name(name)
        number = "147752" + str(time.time())[-5:]
        ccp.input_number(number)
        ccp.hide_keyboard_if_display()
        ccp.input_email_address("a")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0194():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0194_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0194(self):
        """联系-选择一个联系人-编辑-让姓名为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_name("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_number()
        self.assertTrue(ecp.is_toast_exist('姓名不能为空，请输入'))
        ecp.assert_ensure_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0201():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0201_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0201(self):
        """联系-选择一个联系人-编辑-让手机号为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.click_input_number()
        ecp.input_number("")
        ecp.click_input_name()
        self.assertTrue(ecp.is_toast_exist('电话不能为空，请输入'))
        ecp.assert_ensure_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0209():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0209_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0209(self):
        """联系-选择一个联系人-编辑-让公司名为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_company("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0214():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0214_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0214(self):
        """联系-选择一个联系人-编辑-让公司名特殊字符，字母加数字组合"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        name = "Ⅰcom" + str(random.randint(100, 999))
        ecp.input_company(name)
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0216():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0216_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0216(self):
        """联系-选择一个联系人-编辑-让职位为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_position("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0223():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0223_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0223(self):
        """联系-选择一个联系人-编辑-让邮箱为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_email_address("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0228():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0228_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0228(self):
        """联系-选择一个联系人-编辑-让邮箱名为特殊字符，字母加数字组合"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        name = "Ⅰtest" + str(random.randint(100, 999)) + "@Ⅱ" + str(random.randint(100, 999)) + ".com"
        ecp.input_company(name)
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0230():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0230(self):
        """联系-选择一个联系人-编辑-删除联系人"""
        contacts = ContactsPage()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0230_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            name = names[0]
            contacts.select_people_by_name(name)
        cdp.wait_for_page_load()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        ecp.click_delete_contact()
        ecp.click_sure_delete()
        ecp.click_allow_button()
        contacts = ContactsPage()
        time.sleep(2)
        names = contacts.get_all_contacts_name()
        self.assertTrue(name not in names)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0237():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0237_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0237(self):
        """联系-选择一个联系人-分享名片"""
        cdp = ContactDetailsPage()
        cdp.click_share_business_card()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        self.assertTrue(scp.is_element_present_by_locator("搜索或输入手机号"))
        self.assertTrue(scp.is_element_present_by_locator("选择一个群"))
        self.assertTrue(scp.is_element_present_by_locator("选择团队联系人"))
        self.assertTrue(scp.is_element_present_by_locator("选择手机联系人"))
        self.assertTrue(scp.is_element_present_by_locator("最近聊天"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0246():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0246(self):
        """联系-选择一个联系人-点击聊天"""
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        self.assertTrue(single_chat_page.is_on_this_page)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0247():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0247_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0247(self):
        """联系-选择一个联系人-点击电话"""
        cdp = ContactDetailsPage()
        cdp.click_call_icon()
        cdp.click_allow_button()
        time.sleep(3)
        self.assertTrue(current_mobile().is_phone_in_calling_state)
        current_mobile().hang_up_the_call()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0248():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0248_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0248(self):
        """联系-选择一个联系人-点击语音"""
        cdp = ContactDetailsPage()
        cdp.click_voice_call_icon()
        cdp.click_continue_call()
        time.sleep(1)
        self.assertTrue(current_mobile().is_phone_in_calling_state)
        current_mobile().hang_up_the_call()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0250():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0250_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0250(self):
        """联系-选择一个联系人-点击视频电话"""
        cdp = ContactDetailsPage()
        cdp.click_video_call_icon()
        cdp.click_continue_call()
        time.sleep(1)
        self.assertTrue(current_mobile().is_phone_in_calling_state)
        current_mobile().hang_up_the_call()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0259():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0259_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0259(self):
        """联系-选择一个联系人判断是否存在新增桌面快捷方式"""
        cdp = ContactDetailsPage()
        self.assertTrue(cdp.page_contain_shortcut())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0262():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0262_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0262(self):
        """联系-选择联系人-添加桌面快捷方式"""
        cdp = ContactDetailsPage()
        cdp.click_shortcut()
        cdp.click_i_know_and_no_remind()
        cdp.click_allow_button()
        cdp.click_shortcut()
        self.assertTrue(cdp.page_not_contain_i_know())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0291():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0291_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0291(self):
        """联系-选择没有号码的联系人-判断是否存在添加桌面快捷方式"""
        cdp = ContactDetailsPage()
        cdp.click_shortcut()
        cdp.click_i_know_and_no_remind()
        cdp.click_allow_button()
        cdp.click_shortcut()
        self.assertTrue(cdp.is_toast_exist('已添加'))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0352():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0352(self):
        """联系-选择一个联系人-编辑-判断条件"""
        contacts = ContactsPage()
        cdp = ContactDetailsPage()
        # 创建联系人号码部分为+的联系人
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0352_" + str(random.randint(100, 999))
        tail = str(time.time())[-5:]
        number = "++++++" + tail
        ccp.create_contact(name, number)
        ccp.click_allow_button()
        cdp.wait_for_page_load()
        cdp.click_back()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.select_contacts_by_name(name)
        cdp.wait_for_page_load()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        self.assertTrue(ecp.check_element_word("输入号码", "+" + tail))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0353():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0353(self):
        """联系-选择一个联系人-编辑-判断条件"""
        contacts = ContactsPage()
        cdp = ContactDetailsPage()
        # 创建联系人号码全为+的联系人
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0353_" + str(random.randint(100, 999))
        number = "+++++++++++"
        ccp.create_contact(name, number)
        cdp.wait_for_page_load()
        cdp.click_back()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.select_contacts_by_name(name)
        cdp.wait_for_page_load()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        self.assertTrue(ecp.check_element_word("输入号码", "+"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0433():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0433_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back()
            contacts = ContactsPage()
            contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0433(self):
        """联系-标签分组-选择分组-跳转联系人选择器-搜索号码-点击联系人"""
        contacts = ContactsPage()
        names = contacts.get_all_contacts_name()
        self.assertTrue(len(names) > 1)
        contacts.click_label_grouping()
        lgp = LabelGroupingPage()
        lgp.wait_for_page_load()
        # 无分组则创建分组
        group_names = lgp.get_label_grouping_names()
        if len(group_names) == 0:
            group_name = "gtest_0433_" + str(random.randint(100, 999))
            lgp.click_new_create_group()
            time.sleep(1)
            lgp.input_label_grouping_name(group_name)
            lgp.click_sure()
            scp = SelectContactsPage()
            scp.wait_for_page_load()
            scp.click_back()
            lgp = LabelGroupingPage()
            lgp.wait_for_page_load()
            lgp.new_group_click_back()
        else:
            group_name = group_names[0]
        # 点击分组
        lgp.click_label_group(group_name)
        lgdp = LableGroupDetailPage()
        lgdp.wait_for_page_load()
        time.sleep(1)
        lgdp.click_i_know()
        # 点击添加成员
        lgdp.click_add_members()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 全量查询
        scp.click_group_search()
        scp.group_search(names[0])
        if scp.is_keyboard_shown():
            scp.hide_keyboard()
        time.sleep(1)
        # 点击查询结果
        scp.click_search_result_by_name(names[0])
        self.assertTrue(scp.check_if_element_exist("选中联系人头像"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0733():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0733(self):
        """联系-搜索-查看提示词"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.wait_for_page_load()
        clsp.page_should_not_contain_text("本地通讯录")
        clsp.page_should_not_contain_text("和通讯录")
        self.assertFalse(clsp.is_exist_contacts())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0734():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0734(self):
        """联系-搜索-查看提示词"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.wait_for_page_load()
        clsp.page_should_contain_text("输入关键词快速搜索")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0735():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0735(self):
        """联系-搜索-点击返回"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.wait_for_page_load()
        clsp.click_back()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        self.assertTrue(contacts.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0737():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        for i in range(3):
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0737_" + str(random.randint(100, 999))
            number = "147652" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back()
            contacts = ContactsPage()
            contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0737(self):
        """联系-搜索-查看是否有显示更多标识"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.input_search_keyword("atest_0737")
        self.assertFalse(clsp.is_show_more_display())