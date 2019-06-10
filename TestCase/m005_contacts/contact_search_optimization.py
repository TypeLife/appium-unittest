import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.local_contact import localContactPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from preconditions.BasePreconditions import LoginPreconditions
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage

class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()

class ContactSearchOpTest(TestCase):
    """  """
    @classmethod
    def setUpClass(cls):
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.connect_mobile('Android-移动')
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
                required_group_chats = dataproviders.get_preset_group_contacts()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    def default_setUp(self):
        """确保每个用例运行前在收藏页面"""
        # Preconditions.select_mobile('Android-移动')
        # mess = MessagePage()
        # if mess.is_on_this_page():
        #     Preconditions.init_and_enter_collection_page()
        #     return
        # mcp = MeCollectionPage()
        # if mcp.is_on_this_page():
        #     current_mobile().hide_keyboard_if_display()
        #     return
        # else:
        #     current_mobile().launch_app()
        #     Preconditions.init_and_enter_collection_page()
        pass

    def default_tearDown(self):
        lcontact = localContactPage()
        lcontact.set_network_status(6)
        pass

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0010(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("高亮1", "18826200000")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        mess.click_search()
        # 查询页面输入'188262'
        search_page = SearchPage()
        search_number = "188262"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、自动匹配输入结果，搜索内容高亮  准自动化
        # 1.检查搜索结果是否模糊匹配关键字
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0011(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("陈丹丹", "18826211111"), ("alice", "18826211112")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        mess.click_search()
        search_page = SearchPage()
        search_name = "陈丹丹"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 4、出现陈丹丹搜索结果，且陈丹丹高亮 准自动化
        # 1.检查搜索结果是否模糊匹配关键字
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 5、出现alice搜索结果，alice高亮显示
        search_page = SearchPage()
        search_name = "alice"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 6、出现精准搜素结果。18826211111
        search_page = SearchPage()
        search_number = "18826211111"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)
        # 7、不显示团队联系人标签 1999999
        search_page = SearchPage()
        search_number = "1999999"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), False)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0012(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("陈1", "13888137001"), ("陈2", "13801137002"), ('陈3', "13820137003")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        mess.click_search()
        # 查询页面输入'陈'
        search_page = SearchPage()
        search_name = "陈"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、自动匹配输入结果，搜索内容高亮  准自动化
        # 1.检查搜索结果是否模糊匹配关键字
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0015(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("alice", "18826211112"), ("阿啊", "18826211113")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        mess.click_search()
        search_page = SearchPage()
        search_name = "a"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、匹配内容高亮显示，搜索结果显示姓名中包含有a-z，还有包含a-z拼音汉字
        # 3、匹配内容高亮显示，结果也显示包含a结果。
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match("a"), True)
        self.assertEquals(sccp.is_search_contacts_name_match("阿"), True)
        # 2、匹配内容高亮显示，从左至右输入a-al-ali-alic-alice,搜索结果显示正常
        search_page = SearchPage()
        search_name = "alice"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0017(self):

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        mess.click_search()
        # 断开网络
        lcontact = localContactPage()
        lcontact.set_network_status(0)
        # 查询页面输入'大佬1'
        search_page = SearchPage()
        search_page.input_search_keyword("大佬1")
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_toast_exist("当前网络不可用，请检查网络设置"), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0018(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("alice", "18826211112")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        mess.click_search()
        search_page = SearchPage()
        search_name = "alice"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、展示搜索结果，显示头像、姓名、号码（包含其他号码或固话）、公司部门（没公司部门的不显示）
        sccp = SelectCompanyContactsPage()
        search_number = "18826211112"
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        self.assertEquals(sccp.is_exist_select_contacts_image(search_name), True)
        ecp = EnterpriseContactsPage()
        self.assertEquals(ecp.is_exists_value_by_name(search_name), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0736(self):
        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        # 2、输入特殊字符
        mess.click_search()
        # 查询页面输入'+'
        search_page = SearchPage()
        search_page.input_search_keyword('特殊!@$')
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1.模糊匹配到正确的结果
        self.assertEquals(search_page.is_text_present("特殊!@$"), False)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0739(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        # 2、输入特殊字符
        mess.click_search()
        # 查询页面输入'大佬1'
        search_page = SearchPage()
        search_page.input_search_keyword('大佬1')
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1.模糊匹配到正确的结果
        self.assertEquals(search_page.is_text_present("查看更多"), False)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0740(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        # 1、点击通讯录，点击搜索输入框
        # 2、输入特殊字符
        mess.click_search()
        # 查询页面输入'大佬1'
        search_page = SearchPage()
        search_page.input_search_keyword('大佬')
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1.模糊匹配到正确的结果
        self.assertEquals(search_page.is_text_present("查看更多"), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0741(self):
        """查看更多联系人"""
        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        mess.click_search()
        # 查询页面输入'通讯录小于'
        search_page = SearchPage()
        search_page.input_search_keyword('通讯录小于')
        time.sleep(5)
        search_page.hide_keyboard()
        # 1.展示群聊搜索结果标签，标签右上角不展示查看更多按钮
        self.assertEquals(search_page.is_text_present("查看更多"), False)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0742(self):
        Preconditions.make_already_in_message_page()
        # 点击‘通讯录’
        mess = MessagePage()
        mess.open_contacts_page()
        mess.click_search()
        # 查询页面输入'通讯录小于'
        search_page = SearchPage()
        search_page.input_search_keyword('群')
        time.sleep(5)
        search_page.hide_keyboard()
        # 1.展示群聊搜索结果标签，标签右上角展示查看更多按钮  群聊 & 查看更多
        self.assertEquals(search_page.is_text_present("查看更多"), True)

