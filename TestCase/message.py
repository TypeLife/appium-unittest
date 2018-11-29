import unittest
import uuid

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(object):
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
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
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
        one_key.wait_for_tell_number_load(30)
        login_number = one_key.get_login_number()
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)
        return login_number

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
    def make_already_in_message_page(reset_required=False):
        """
        前置条件：
        1.已登录客户端
        2.当前在消息页面
        """
        if not reset_required:
            message_page = MessagePage()
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
        Preconditions.login_by_one_key_login()


@unittest.skip
class MessageTest(TestCase):
    """Message 模块"""

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    def test_something(self):
        """description"""
        self.assertEqual(True, False)

    def setUp_test_something(self):
        print("Run test case setup.")


class MessageSearchTest(TestCase):
    """消息-全局搜索"""

    @tags('ALL', 'SMOKE')
    def test_msg_search_0001(self):
        """消息-消息列表界面搜索框显示"""
        message = MessagePage()
        message.assert_search_box_is_display(8)

    @staticmethod
    def setUp_test_msg_search_0001():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0002(self):
        """搜索框正常弹起和收起"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        search_page.assert_keyboard_is_display(5)
        search_page.hide_keyboard()
        search_page.assert_keyboard_is_hided()

    @staticmethod
    def setUp_test_msg_search_0002():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @staticmethod
    def tearDown_test_msg_search_0002():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0003(self):
        """搜索关键字"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '陈'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 联系人数量
        contact_count = 0
        # 群聊数量
        group_chat_count = 0
        # 聊天记录数量
        chat_count = 0
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if category == 0:
                if now_go_to == '联系人':
                    contact_count += 1
                elif now_go_to == '群聊':
                    group_chat_count += 1
                elif now_go_to == '聊天记录':
                    chat_count += 1
                else:
                    pass
        self.assertGreater(contact_count, 0, '匹配到有关“{}”的联系人信息'.format(search_key))
        self.assertEqual(chat_count, 0, '聊天记录不为空')
        self.assertEqual(group_chat_count, 0, '群聊记录群聊记录不为空')

    @staticmethod
    def setUp_test_msg_search_0003():
        """
        1、联网正常
        2、首次登录客户端，没有群聊和聊天记录
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=True)

    @staticmethod
    def tearDown_test_msg_search_0003():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0004(self):
        """搜索关键字"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '群'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 联系人数量
        contact_count = 0
        # 群聊数量
        group_chat_count = 0
        # 聊天记录数量
        chat_count = 0
        # 列表顺序【联系人】-【群聊】-【聊天记录】板块顺序
        list_order = []
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
                if category in ['联系人', '群聊', '聊天记录']:
                    list_order.append(category)
            if category == 0:
                if now_go_to == '联系人':
                    contact_count += 1
                elif now_go_to == '群聊':
                    group_chat_count += 1
                elif now_go_to == '聊天记录':
                    chat_count += 1
                else:
                    pass
        self.assertLessEqual(contact_count, 3, '匹配到有关“{}”的联系人信息'.format(search_key))
        self.assertLessEqual(chat_count, 3, '聊天记录不为空')
        self.assertLessEqual(group_chat_count, 3, '群聊记录群聊记录不为空')
        if len(list_order) > 0:
            self.assertEqual(list_order[0], '联系人')
        if len(list_order) > 1:
            self.assertEqual(list_order[1], '群聊')
        if len(list_order) > 2:
            self.assertEqual(list_order[2], '聊天记录')

    @staticmethod
    def setUp_test_msg_search_0004():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0004():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0005(self):
        """会话窗口点击后退"""

        # 先创建一个名字唯一的联系人名并发一条内容唯一的消息文本
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.click_add()

        create_page = CreateContactPage()
        uid = uuid.uuid4().__str__()
        number = '17611681917'

        create_page.hide_keyboard_if_display()
        create_page.create_contact(uid, number)

        detail_page = ContactDetailsPage()
        detail_page.click_message_icon()

        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        message_content = uuid.uuid4().__str__()
        chat.send_message(message_content)

        # 返回消息页并进入搜索页面
        chat.click_back()
        detail_page.click_back_icon()
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 输入关键字进行搜索
        search_key = uid
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()

        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to == '联系人' and category == 0:
                result.click()
                break
        detail_page.wait_for_page_load()
        detail_page.click_message_icon()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        chat.assert_message_content_display(message_content)
        chat.click_back()
        detail_page.click_back_icon()
        # 检查搜索关键字
        search_page.wait_for_page_load()
        search_page.assert_current_search_keyword_is(search_key)

    @staticmethod
    def setUp_test_msg_search_0005():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0005():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0006(self):
        """搜索关键字-精准搜索"""

        # 先创建一个名字唯一的联系人名并发一条内容唯一的消息文本

        # 通讯录页
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.click_add()

        # 新建联系人页
        create_page = CreateContactPage()
        uid = uuid.uuid4().__str__()
        number = '17611681917'
        create_page.hide_keyboard_if_display()
        create_page.create_contact(uid, number)

        # 联系人详情页
        detail_page = ContactDetailsPage()
        detail_page.click_message_icon()

        # 聊天页
        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        message_content = '吃饭啊'
        chat.send_message(message_content)

        # 返回消息页并进入搜索页面
        chat.click_back()
        detail_page.click_back_icon()

        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = message_content
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to == '联系人' and category == 0:
                # 检查搜索结果是否完全匹配关键字
                search_page.assert_search_result_full_match_keyword(result, search_key)

    @staticmethod
    def setUp_test_msg_search_0006():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0006():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0007(self):
        """搜索关键字-中文模糊搜索"""

        # 先创建一个名字唯一的联系人名并发一条内容唯一的消息文本

        # 通讯录页
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.click_add()

        # 新建联系人页
        create_page = CreateContactPage()
        uid = uuid.uuid4().__str__()
        number = '17611681917'
        create_page.hide_keyboard_if_display()
        create_page.create_contact(uid, number)

        # 联系人详情页
        detail_page = ContactDetailsPage()
        detail_page.click_message_icon()

        # 聊天页
        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        message_content = '吃饭啊'
        chat.send_message(message_content)

        # 返回消息页并进入搜索页面
        chat.click_back()
        detail_page.click_back_icon()

        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = message_content[:-1]
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to == '联系人' and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @staticmethod
    def setUp_test_msg_search_0007():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0007():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0008(self):
        """搜索关键字-英文模糊搜索"""

        # 先创建一个名字唯一的联系人名并发一条内容唯一的消息文本

        # 通讯录页
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.click_add()

        # 新建联系人页
        create_page = CreateContactPage()
        uid = uuid.uuid4().__str__()
        number = '17611681917'
        create_page.hide_keyboard_if_display()
        create_page.create_contact(uid, number)

        # 联系人详情页
        detail_page = ContactDetailsPage()
        detail_page.click_message_icon()

        # 聊天页
        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        a_to_z = 'abcDEFghijklmnopqrstuvwxyz'
        message_content = '其他字符' + a_to_z + '其他字符'
        chat.send_message(message_content)

        # 返回消息页并进入搜索页面
        chat.click_back()
        detail_page.click_back_icon()

        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = a_to_z.lower()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to == '联系人' and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @staticmethod
    def setUp_test_msg_search_0008():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0008():
        search_page = SearchPage()
        search_page.click_back_button()
