import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.local_contact import localContactPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from library.core.utils.applicationcache import current_mobile

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

class Preconditions(WorkbenchPreconditions):
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

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client


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
        # 6、出现精准搜素结果。13800137003
        search_page = SearchPage()
        search_number = "13800137003"
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
    def test_contacts_quxinli_0013(self):
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
        mess.click_search()
        search_page = SearchPage()
        search_number = "8"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、搜索匹配内容显示高亮
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)
        # 2、输入1-11位同我的团队匹配号码，18826211112
        search_page = SearchPage()
        search_number = "18826211112"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0014(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296")]
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
        mess.click_search()
        search_page = SearchPage()
        search_number = "+861882"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、搜索结果显示所有匹配到号码
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)

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
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296")]
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
    def test_contacts_quxinli_0016(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296"), ('测试啊2', "#*13800137004")]
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
        search_number = "#*"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、1、搜索出对应联系人，排序按照平台返回的搜索结果排序
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)

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
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296"), ('测试啊2', "#*13800137004")]
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
    def test_contacts_quxinli_0025(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296"), ('测试啊2', "#*13800137004")]
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
        search_number = "1882621"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、自动匹配输入结果，搜索内容高亮
        # 2、结果显示所有企业下匹配的人员
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0026(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296"), ('测试啊2', "#*13800137004")]
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
        # 4、出现陈丹丹搜索结果，且陈丹丹高亮。
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_name), True)

        search_name = "alice"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        # 5、出现alice搜索结果，alice高亮显示
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_name), True)

        search_number = "13802883296"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 6、出现精准搜素结果。13802883296高亮显示
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)

        search_number = "138028"
        search_page.input_search_keyword(search_number)
        time.sleep(5)
        search_page.hide_keyboard()
        # 7、出现无此联系人提示
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), False)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0027(self):
        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "18826211112"), ('郑海', "13802883296"),
                                  ('测试啊', "+8618822883296"), ('测试啊2', "#*13800137004")]
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
        search_name = "测试"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        # 判定点
        # 1、自动匹配输入结果，搜索内容高亮  准自动化
        # 1.检查搜索结果是否模糊匹配关键字
        sccp = SelectCompanyContactsPage()
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)

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
        self.assertEquals(search_page.is_text_present("大佬1"), False)

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
        # 点击‘联系’
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

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0743(self):
        Preconditions.make_already_in_message_page()
        # 点击‘联系’
        mess = MessagePage()
        mess.open_contacts_page()
        mess.click_search()
        # 查询页面输入'和飞信团队''
        search_page = SearchPage()
        search_page.input_search_keyword('和飞信团队')
        time.sleep(5)
        search_page.hide_keyboard()
        # 1.展示公众号搜索结果标签，标签右上角不展示查看更多按钮
        self.assertEquals(search_page.is_text_present("查看更多"), False)
        self.assertEquals(search_page.is_text_present("公众号"), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0744(self):
        Preconditions.make_already_in_message_page()
        # 点击‘联系’
        mess = MessagePage()
        mess.open_contacts_page()
        mess.click_search()
        # 查询页面输入'和'
        search_page = SearchPage()
        search_page.input_search_keyword('和')
        time.sleep(5)
        search_page.hide_keyboard()
        # 展示公众号搜索结果标签，标签右上角展示查看更多按钮
        self.assertEquals(search_page.is_text_present("查看更多"), True)
        self.assertEquals(search_page.is_text_present("公众号"), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0760(self):
        Preconditions.make_already_in_message_page()
        # 点击‘联系’
        mess = MessagePage()
        mess.open_contacts_page()
        mess.click_search()
        # 查询页面输入'和飞信1'
        search_page = SearchPage()
        search_page.input_search_keyword('和飞信1')
        time.sleep(5)
        search_page.hide_keyboard()
        # 搜索时，不展示和通讯录搜索结果标签
        self.assertEquals(search_page.is_text_present("无搜索结果"), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_chenjixiang_0781(self):
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
        self.assertEquals(search_page.is_text_present("大佬1"), False)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0004(self):
        Preconditions.make_already_in_message_page()
        # 点击‘联系’
        mess = MessagePage()
        mess.open_contacts_page()
        time.sleep(5)
        # 1、联系页面从上到下依次为搜索栏，
        # 2、备份手机联系提示：备份你的手机联系，联系人数据不丢失
        # 3、顶部入口：群聊、公众号，创建团队
        contact = ContactsPage()
        self.assertEquals(contact.is_exist_search_view(), True)
        search_page = SearchPage()
        self.assertEquals(search_page.is_text_present("备份你的手机联系，联系人数据不丢失"), True)
        self.assertEquals(search_page.is_text_present("群聊"), True)
        self.assertEquals(search_page.is_text_present("公众号"), True)
        self.assertEquals(search_page.is_text_present("创建团队"), True)

    @tags('ALL', 'CONTACT', 'YL')
    def test_contacts_quxinli_0024(self):
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
        search_name = "哈 马上"
        search_page.input_search_keyword(search_name)
        time.sleep(5)
        search_page.hide_keyboard()
        SelectHeContactsDetailPage().selecting_he_contacts_by_name(search_name)
        time.sleep(1)
        # 判定点
        # 进入个人详情页 判断页面包含的元素
        detailpage = ContactDetailsPage()
        # 名字
        detailpage.is_exists_contacts_name()
        # 号码
        detailpage.is_exists_contacts_number()
        # detailpage.page_should_contain_text('B')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        # 消息、电话、语音视频、视频电话、副号拨打、和飞信电话置灰，不可点击
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('和飞信电话')
        time.sleep(2)
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()
        time.sleep(2)
        # 返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

