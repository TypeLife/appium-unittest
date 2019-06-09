import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import LoginPreconditions


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

class MsgSelectMoreTest(TestCase):
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
                required_group_chats = dataproviders.get_preset_group_chats()
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
        pass

    @tags('ALL', 'SMOKE')
    def test_msg_huangcaizui_E_0017(self):
        """查看更多联系人"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search()
        search_page = SearchPage()
        search_page.input_search_keyword('大佬')
        time.sleep(5)
        select_contacts = SelectContactsPage()
        select_contacts.hide_keyboard()
        select_contacts.click_read_more()
        time.sleep(5)
        # 判定点
        # 1.搜索结果显示相应匹配的联系人信息
        select_contacts.is_text_present("大佬1")
        # 2.跳转到搜索到的所有联系人显示页面
        select_contacts.is_text_present("手机联系人")

    @tags('ALL', 'SMOKE')
    def test_msg_huangcaizui_E_0020(self):
        """查看更多联系人"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search()
        search_page = SearchPage()
        search_page.input_search_keyword('群')
        time.sleep(5)
        select_contacts = SelectContactsPage()
        select_contacts.hide_keyboard()
        # 群聊 & 查看更多
        # select_contacts.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @index="2"]'))
        select_contacts.click_read_more()
        time.sleep(5)
        # 判定点
        # 1.搜索结果显示相关匹配的群聊名称；
        select_contacts.is_text_present("群聊1")
        # 2.跳转到搜索到的所有群聊信息页面
        self.assertEquals(select_contacts.is_text_present("查看更多"), False)
