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
                # for name, number in required_contacts:
                #     # 创建联系人
                #     conts.create_contacts_if_not_exits(name, number)
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
        pass

    @tags('ALL', 'SMOKE')
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
        # 判定点
        # 1.展示群聊搜索结果标签，标签右上角不展示查看更多按钮
        self.assertEquals(search_page.is_text_present("查看更多"), False)

        @tags('ALL', 'SMOKE')
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
            # 判定点
            # 1.展示群聊搜索结果标签，标签右上角展示查看更多按钮  群聊 & 查看更多
            self.assertEquals(search_page.is_text_present("查看更多"), True)

