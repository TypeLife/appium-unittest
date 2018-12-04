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
        order_map = {
            '联系人': 1,
            '群聊': 2,
            '聊天记录': 3,
            '公众号': 4,
        }
        value_map = {
            1: '联系人',
            2: '群聊',
            3: '聊天记录',
            4: '公众号',
        }
        list_order = []
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
                list_order.append(order_map.get(category))
                # if category in ['联系人', '群聊', '聊天记录']:
                #     list_order.append(category)
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

        sorted_order = list_order.copy()
        sorted_order.sort()
        self.assertEqual(list_order, sorted_order, '排序"{}"'.format([value_map[i] for i in list_order]))

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

    @tags('ALL', 'SMOKE')
    def test_msg_search_0009(self):
        """搜索关键字-数字模糊搜索"""

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
        one_to_ziro = '1234567890'
        message_content = '其他字符' + one_to_ziro + '其他字符'
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
        search_key = one_to_ziro
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['联系人', '群聊', '聊天记录', '公众号'] and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @staticmethod
    def setUp_test_msg_search_0009():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0009():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0010(self):
        """搜索关键字-特殊字符模糊搜索"""

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
        special_characters = '#@￥%'
        message_content = '其他字符' + special_characters + '其他字符'
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
        search_key = special_characters
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        for result in search_page.iterate_list():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['联系人', '群聊', '聊天记录', '公众号'] and category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @staticmethod
    def setUp_test_msg_search_0010():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0010():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0011(self):
        """搜索不存在的关键字"""

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
        search_key = '奇货可居'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()

        # 检查无结果提示是否显示
        search_page.assert_no_result_tips_display()
        # 检查搜索和通讯录联系人入口是否显示
        search_page.assert_hetongxunlu_entry_is_display()

    @staticmethod
    def setUp_test_msg_search_0011():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0011():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0012(self):
        """搜索聊天记录版块不存在的关键字"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        contact_results = []
        group_chat_results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                self.assertNotEqual(category, '聊天记录', '检查点："聊天记录"板块不展示')
                now_go_to = category
            if now_go_to in ['联系人'] and category == 0:
                # 检查搜索结果是否包含关键字
                contact_results.append(result)
            if now_go_to in ['群聊'] and category == 0:
                # 检查搜索结果是否包含关键字
                group_chat_results.append(result)
        self.assertEqual(len(contact_results), 3, '搜索结果中，联系人数量不正确')
        self.assertEqual(len(group_chat_results), 3, '搜索结果中，群聊数量不正确')

    @staticmethod
    def setUp_test_msg_search_0012():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        for group_name in [key_message + '1', key_message + '2', key_message + '3', key_message + '4']:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_back()
            else:
                group_search.click_back()
                group_list.click_create_group()
                select_page = SelectContactPage()
                select_page.search_and_select_contact('13922996261', '13922996262')
                build_page = BuildGroupChatPage()
                build_page.create_group_chat(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.click_back()

        group_list.click_back()

        # 创建联系人
        names = [key_message + '1', key_message + '2', key_message + '3', key_message + '4']
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_back()
            else:
                contact_search.click_back()
                contacts_page.click_add()
                create_page = CreateContactPage()
                number = '1380013800{}'.format(names.index(uid))
                create_page.hide_keyboard_if_display()
                create_page.create_contact(uid, number)
                detail_page = ContactDetailsPage()
                detail_page.click_back_icon()

    @staticmethod
    def tearDown_test_msg_search_0012():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0013(self):
        """搜索群聊版块不存在的关键字"""
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        contact_results = []
        chat_history = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                self.assertNotEqual(category, '群聊', '检查点："群聊"板块不展示')
                now_go_to = category
            if now_go_to in ['联系人'] and category == 0:
                # 检查搜索结果是否包含关键字
                contact_results.append(result)
            if now_go_to in ['聊天记录'] and category == 0:
                # 检查搜索结果是否包含关键字
                chat_history.append(result)
        self.assertEqual(len(contact_results), 3, '检查点：联系人最多显示3条')
        self.assertEqual(len(chat_history), 3, '检查点：聊天记录最多显示3条')

    @staticmethod
    def setUp_test_msg_search_0013():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        for group_name in ['群聊1', '群聊2', '群聊3', '群聊4']:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                group_search.click_back()
                group_list.click_create_group()
                select_page = SelectContactPage()
                select_page.search_and_select_contact('13922996261', '13922996262')
                build_page = BuildGroupChatPage()
                build_page.create_group_chat(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back()

        group_list.click_back()

        # 创建联系人
        names = [key_message + '1', key_message + '2', key_message + '3', key_message + '4']
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_back()
            else:
                contact_search.click_back()
                contacts_page.click_add()
                create_page = CreateContactPage()
                number = '1380013800{}'.format(names.index(uid))
                create_page.hide_keyboard_if_display()
                create_page.create_contact(uid, number)
                detail_page = ContactDetailsPage()
                detail_page.click_back_icon()

    @staticmethod
    def tearDown_test_msg_search_0013():
        search_page = SearchPage()
        search_page.click_back_button() @ tags('ALL', 'SMOKE')

    @tags('ALL', 'SMOKE')
    def test_msg_search_0014(self):
        """搜索联系人排序"""
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                self.assertNotEqual(category, '群聊', '检查点："群聊"板块不展示')
                now_go_to = category
            if now_go_to in ['联系人'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                results.append(name)
        self.assertEqual(results[0], '大佬2', '检查点：搜索结果中联系人版块排序是：最近生成消息的联系人')
        self.assertEqual(results[1], '大佬1', '检查点：聊天记录最多显示3条')

    @staticmethod
    def setUp_test_msg_search_0014():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()
        # 创建联系人
        names = [key_message + '1', key_message + '2']
        for uid in names:
            contacts_page.click_search_box()
            contact_search = ContactListSearchPage()
            contact_search.wait_for_page_load()
            contact_search.input_search_keyword(uid)
            if contact_search.is_contact_in_list(uid):
                contact_search.click_contact(uid)
                detail_page.click_message_icon()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message('新消息')
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                contact_search.click_back()
                contacts_page.click_add()
                create_page = CreateContactPage()
                number = '1380013800{}'.format(names.index(uid))
                create_page.hide_keyboard_if_display()
                create_page.create_contact(uid, number)
                detail_page.click_message_icon()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message('新消息')
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                # detail_page.click_back_icon()

    @staticmethod
    def tearDown_test_msg_search_0014():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0015(self):
        """搜索群聊排序"""
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        for group_name in ['群聊1', '群聊2']:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                group_search.click_back()
                group_list.click_create_group()
                select_page = SelectContactPage()
                select_page.search_and_select_contact('13922996261', '13922996262')
                build_page = BuildGroupChatPage()
                build_page.create_group_chat(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back()
        group_list.click_back()
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.set_top_for_message('群聊1')
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = '群聊'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['群聊'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                results.append(name)
        self.assertEqual(results[0], '群聊2', '检查点：搜索结果中群聊排序是：最近生成消息的群聊（按时间排序）')
        self.assertEqual(results[1], '群聊1', '检查点：搜索结果中群聊排序是：最近生成消息的群聊（按时间排序）')

    @staticmethod
    def setUp_test_msg_search_0015():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0015():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0016(self):
        """搜索聊天记录排序"""
        key_message = '新消息'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        for group_name in ['群聊1', '群聊2']:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                group_search.click_back()
                group_list.click_create_group()
                select_page = SelectContactPage()
                select_page.search_and_select_contact('13922996261', '13922996262')
                build_page = BuildGroupChatPage()
                build_page.create_group_chat(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(key_message)
                chat.click_back()
        group_list.click_back()
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.set_top_for_message('群聊1')
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                results.append(name)
        self.assertEqual('群聊2', results[0], '检查点：搜索结果中聊天记录排序是： 按时间排序')
        self.assertEqual('群聊1', results[1], '检查点：搜索结果中聊天记录排序是： 按时间排序')

    @staticmethod
    def setUp_test_msg_search_0016():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0016():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0017(self):
        """查看更多联系人"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['联系人'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                self.assertIn(search_key, name)
                results.append(name)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相应匹配的联系人信息')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '联系人':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)

        show_more = GlobalSearchContactPage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @staticmethod
    def setUp_test_msg_search_0017():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0017():
        show_more = GlobalSearchContactPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0018(self):
        """清空搜索条件"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        search_page.input_search_keyword('关键字')
        search_page.click_clear_keyword_button()
        # 检查点: 置灰语：搜索
        search_page.assert_current_search_keyword_is('输入关键词快速搜索')
        search_page.click_back_button()
        message_page.assert_search_box_text_is('搜索')

    @staticmethod
    def setUp_test_msg_search_0018():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0019(self):
        """更改搜索关键字"""
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = '测试'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 更换关键字
        search_key = '给个红包'
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示

        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == 0:
                # 检查搜索结果是否包含关键字
                search_page.assert_search_result_match_keyword(result, search_key)

    @staticmethod
    def setUp_test_msg_search_0019():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @staticmethod
    def tearDown_test_msg_search_0019():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0020(self):
        """查看更多群聊"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['群聊'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                search_page.assert_search_result_match_keyword(result, search_key)
                self.assertIn(search_key, name)
                results.append(name)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关匹配的群聊名称；')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '群聊':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)

        show_more = GlobalSearchGroupPage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @staticmethod
    def setUp_test_msg_search_0020():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0020():
        show_more = GlobalSearchGroupPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE')
    def test_msg_search_0021(self):
        """查看更多群聊"""
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.click_search()

        # 全局搜索页
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 用消息内容作为关键字搜索
        search_key = key_message
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        now_go_to = None
        # 聊天记录是否显示
        results = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['群聊'] and category == 0:
                # 检查搜索结果是否包含关键字
                name = search_page.get_contact_name(result)
                search_page.assert_search_result_match_keyword(result, search_key)
                self.assertIn(search_key, name)
                results.append(name)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关匹配的群聊名称；')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '群聊':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)

        show_more = GlobalSearchGroupPage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')
        show_more.clear_search_keyword()
        search_key = key_message + '1'
        show_more.search(search_key)
        show_more.hide_keyboard_if_display()
        show_more.assert_list_contains_group(search_key)

    @staticmethod
    def setUp_test_msg_search_0021():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        Preconditions.connect_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_search_0021():
        show_more = GlobalSearchGroupPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()
