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