import unittest
import uuid
import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
import preconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class MessageScanTest(TestCase):
    """消息 - 扫一扫"""

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_A_0014(self):
        """网络异常使用扫一扫"""
        message_page = MessagePage()
        message_page.click_add_icon()
        message_page.click_take_a_scan()
        time.sleep(8)

        scan_page = Scan1Page()
        # scan_page.wait_for_page_load()
        scan_page.assert_network_disconnect_img_is_display()

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0014():
        """
        1.网络异常
        2.已登录客户端
        3.当前在消息列表界面
        4.使用扫一扫功能
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        current_mobile().set_network_status(0)
        current_mobile().activate_app()

    @staticmethod
    def tearDown_test_msg_xiaoliping_A_0014():
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().set_network_status(6)
        scan_page = Scan1Page()
        scan_page.click_back()
        current_mobile().activate_app()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_A_0026(self):
        """进入我的二维码页面"""
        message_page = MessagePage()
        message_page.click_add_icon()
        message_page.click_take_a_scan()

        scan_page = ScanPage()
        scan_page.wait_for_page_load()
        time.sleep(2)
        scan_page.open_my_qr_code_page()
        time.sleep(2)

        qr_code_page = MyQRCodePage()
        qr_code_page.wait_for_loading_animation_end()

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0026():
        """
        1.网络正常
        2.已登录客户端
        3.当前在消息列表界面
        4.使用扫一扫功能
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @staticmethod
    def tearDown_test_msg_xiaoliping_A_0026():
        qr_code_page = MyQRCodePage()
        qr_code_page.click_back()
        scan_page = ScanPage()
        scan_page.click_back()


class MessageSearchTest(TestCase):
    """消息-全局搜索"""

    @classmethod
    def setUpClass(cls):

        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
                current_mobile().hide_keyboard_if_display()
                for name, number in required_contacts:
                    preconditions.make_already_in_message_page()
                    conts.open_contacts_page()
                    conts.create_contacts_if_not_exits(name, number)

                # 创建群
                required_group_chats = dataproviders.get_preset_group_chats()

                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    @tags('ALL', 'SMOKE', "CMCC1")
    def test_msg_huangcaizui_E_0001(self):
        """消息-消息列表界面搜索框显示"""
        message = MessagePage()
        message.assert_search_box_is_display(8)

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0001():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0002(self):
        """搜索框正常弹起和收起"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        search_page.assert_keyboard_is_display(5)
        search_page.hide_keyboard()
        search_page.assert_keyboard_is_hided()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0002():
        """
        1、联网正常
        2、已登录客户端
        3、当前在消息页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0002():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0003(self):
        """搜索联系人"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '茻'
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
        self.assertGreater(contact_count, 0, '检查点：搜索匹配到的全部有关“{}”的联系'.format(search_key))
        self.assertEqual(chat_count, 0, '检查点：聊天记录为空')
        self.assertEqual(group_chat_count, 0, '检查点：群聊为空')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0003():
        """
        1、联网正常
        2、首次登录客户端，没有群聊和聊天记录
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0003():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0004(self):
        """搜索关键字-精准搜索"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '给个红包'
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
        self.assertLessEqual(contact_count, 3, '检查点：联系人版块各显示不超过三条')
        self.assertLessEqual(chat_count, 3, '检查点：聊天记录版块各显示不超过三条')
        self.assertLessEqual(group_chat_count, 3, '检查点：群聊版块各显示不超过三条')

        sorted_order = list_order.copy()
        sorted_order.sort()
        self.assertEqual(list_order, sorted_order, '排序"{}"'.format([value_map[i] for i in list_order]))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0004():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0004():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0005(self):
        """会话窗口点击后退"""
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()
        message_page = MessagePage()
        message_page.open_message_page()
        message_page.scroll_to_top()
        message_page.click_search()
        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()

        # 输入关键字进行搜索
        search_key = self.contact_name
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
        chat.assert_message_content_display(self.message_content)
        chat.click_back()
        detail_page.click_back_icon()
        # 检查搜索关键字
        search_page.wait_for_page_load()
        search_page.assert_current_search_keyword_is(search_key)

    def setUp_test_msg_huangcaizui_E_0005(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 发送消息
        self.contact_name = '给个红包1'
        self.message_content = uuid.uuid4().__str__()
        contacts_page.open_contacts_page()
        names = [self.contact_name]
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
                chat.send_message(self.message_content)
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0005():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0006(self):
        """搜索关键字-精准搜索"""
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
        search_key = self.message_content
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

    def setUp_test_msg_huangcaizui_E_0006(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.message_content = '吃饭啊'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
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
                chat.send_message(self.message_content)
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0006():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0007(self):
        """搜索关键字-中文模糊搜索"""

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
        search_key = self.message_content[:-1]
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

    def setUp_test_msg_huangcaizui_E_0007(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.message_content = '巴适得板'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
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
                chat.send_message(self.message_content)
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0007():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0008(self):
        """搜索关键字-英文模糊搜索"""

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
        search_key = self.search_keyword.lower()
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

    def setUp_test_msg_huangcaizui_E_0008(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.search_keyword = 'abcDEFghijklmnopqrstuvwxyz'
        self.message_content = '其他字符' + self.search_keyword + '其他字符'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
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
                chat.send_message(self.message_content)
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0008():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0009(self):
        """搜索关键字-数字模糊搜索"""

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
        search_key = self.search_keyword
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

    def setUp_test_msg_huangcaizui_E_0009(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.search_keyword = '1234567890'
        self.message_content = '其他字符' + self.search_keyword + '其他字符'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
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
                chat.send_message(self.message_content)
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0009():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0010(self):
        """搜索关键字-特殊字符模糊搜索"""

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
        search_key = self.search_keyword
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

    def setUp_test_msg_huangcaizui_E_0010(self):
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        chat = ChatWindowPage()

        # 创建联系人
        self.contact_name = '给个红包1'
        self.search_keyword = '#@￥%'
        self.message_content = '其他字符' + self.search_keyword + '其他字符'
        contacts_page.open_contacts_page()
        names = [self.contact_name]
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
                chat.send_message(self.message_content)
                chat.click_back()
                detail_page.wait_for_page_load()
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(self.contact_name))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0010():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0011(self):
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
        # search_page.assert_no_result_tips_display()
        # 检查搜索和通讯录联系人入口是否显示
        search_page.assert_group_entry_is_display()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0011():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0011():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0012(self):
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
    def setUp_test_msg_huangcaizui_E_0012():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        key_message = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = [key_message + '1', key_message + '2', key_message + '3', key_message + '4']
        for group_name in groups:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))

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
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(names))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0012():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0013(self):
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
    def setUp_test_msg_huangcaizui_E_0013():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = ['群聊1', '群聊2', '群聊3', '群聊4']
        for group_name in groups:
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
                time.sleep(2)
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))

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
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(names))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0013():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0014(self):
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
    def setUp_test_msg_huangcaizui_E_0014():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
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
                time.sleep(2)
                detail_page.click_back_icon()
                contact_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到联系人"{}"'.format(names))

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0014():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0015(self):
        """搜索群聊排序"""

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
    def setUp_test_msg_huangcaizui_E_0015():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        key_message = '大佬'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = ['群聊1', '群聊2']
        for group_name in groups:
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
                time.sleep(2)
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))
        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_search_0015():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0016(self):
        """搜索聊天记录排序"""
        key_message = '新消息'
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
    def setUp_test_msg_huangcaizui_E_0016():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

        key_message = '新消息'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        groups = ['群聊1', '群聊2']
        for group_name in groups:
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
                time.sleep(2)
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(groups))
        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_search_0016():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0017(self):
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
        time.sleep(2)
        search_page.click_show_more(searching)

        show_more = GlobalSearchContactPage()
        try:
            time.sleep(4)
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0017():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0017():
        show_more = GlobalSearchContactPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0018(self):
        """清空搜索条件"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        search_page.input_search_keyword('关键字')
        search_page.click_clear_keyword_button()
        # 检查点: 置灰语：搜索
        search_page.assert_current_search_keyword_is('搜索')
        search_page.click_back_button()
        message_page.assert_search_box_text_is('搜索')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0018():
        """
        1、联网正常
        2、已登录客户端
        3、当前联系人搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0019(self):
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
    def setUp_test_msg_huangcaizui_E_0019():
        """
        1、联网正常
        2、已登录客户端
        3、当前联系人搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0019():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0020(self):
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
            time.sleep(2)
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0020():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0020():
        show_more = GlobalSearchGroupPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0021(self):
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
            time.sleep(3)
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')
        show_more.clear_search_keyword()
        search_key = key_message + '1'
        show_more.search(search_key)
        show_more.hide_keyboard_if_display()
        show_more.assert_list_contains_group(search_key)

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0021():
        """
        1、联网正常
        2、已登录客户端
        3、当前群聊搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0021():
        show_more = GlobalSearchGroupPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0022(self):
        """查看更多聊天记录"""
        key_message = '聊'
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
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, search_key)
                results.append(result)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关聊天记录的联系人名称或群聊名称')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '聊天记录':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)
        show_more = GlobalSearchMessagePage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0022():
        """
        1、联网正常
        2、已登录客户端
        3、当前群聊搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.click_contacts()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1', group_name + '2', group_name + '3', group_name + '4']
        for group_name in group_names:
            chat_message = '聊天记录搜索测试{}'.format(group_names.index(group_name))
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(chat_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))
        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0022():
        show_more = GlobalSearchGroupPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0023(self):
        """查看更多聊天记录"""
        key_message = '聊'
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
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, search_key)
                results.append(result)
        self.assertEqual(3, len(results), '检查点：搜索结果显示相关聊天记录的联系人名称或群聊名称')

        search_page.click_clear_keyword_button()
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        # 聊天记录是否显示
        searching = None
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category == '聊天记录':
                searching = result
                # 检查是否显示查看更多入口
                search_page.assert_show_more_is_display(result)
                break
        self.assertIsNotNone(searching, '页面应该显示"联系人"板块')
        search_page.click_show_more(searching)
        show_more = GlobalSearchMessagePage()
        try:
            show_more.wait_for_page_load()
        except TimeoutException:
            raise AssertionError('查看更多联系人页面没有打开')
        show_more.clear_search_keyword()
        search_key = '聊天记录搜索测试' + '1'
        show_more.search(search_key)
        show_more.hide_keyboard_if_display()
        show_more.assert_list_contains_message(search_key)

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0023():
        """
        1、联网正常
        2、已登录客户端
        3、当前群聊搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1', group_name + '2', group_name + '3', group_name + '4']
        for group_name in group_names:
            chat_message = '聊天记录搜索测试{}'.format(group_names.index(group_name))
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                chat.send_message(chat_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0023():
        show_more = GlobalSearchGroupPage()
        show_more.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0024(self):
        """查看更多聊天记录"""
        key_message = '测试相同聊天记录大于一条'
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
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, "2条相关聊天记录")
                results.append(result)
        self.assertEqual(1, len(results), '检查点：搜索结果显示相关聊天记录的联系人名称或群聊名称')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0024():
        """
        1、联网正常
        2、已登录客户端
        3、当前聊天页面搜索页面
        4、同一个群或联系人有多条相同的聊天记录
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1']
        for group_name in group_names:
            chat_message = '测试相同聊天记录大于一条'
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                # 发第一次
                chat.send_message(chat_message)
                # 发第二次
                chat.send_message(chat_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0024():
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_msg_huangcaizui_E_0025(self):
        """查看更多聊天记录"""
        key_message = '测试相同聊天记录大于一条'
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
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category in ['联系人', '群聊', '聊天记录', '公众号']:
                now_go_to = category
            if now_go_to in ['聊天记录'] and category == 0:
                # 搜索结果显示相关聊天记录的联系人名称或群聊名称
                search_page.assert_search_result_match_keyword(result, "2条相关聊天记录")
                result.click()

        message_search = MessageSearchPage()
        message_search.wait_for_page_load()
        message_search.assert_list_data_match_statistic_bar()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0025():
        """
        1、联网正常
        2、已登录客户端
        3、当前聊天页面搜索页面
        4、同一个群或联系人有多条相同的聊天记录
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=True)
        group_name = '给个红包'
        # 消息页
        message_page = MessagePage()

        # 创建群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        group_names = [group_name + '1']
        for group_name in group_names:
            chat_message = '测试相同聊天记录大于一条'
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                # 发第一次
                chat.send_message(chat_message)
                # 发第二次
                chat.send_message(chat_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0025():
        message_search = MessageSearchPage()
        message_search.click_back()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC")
    def test_msg_huangcaizui_E_0026(self):
        """网络异常全局搜索"""
        message_page = MessagePage()
        message_page.scroll_to_top()
        message_page.click_search()

        search_page = SearchPage()
        if search_page.mobile.is_keyboard_shown():
            search_page.hide_keyboard()
        search_key = '给个红包'
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
    def setUp_test_msg_huangcaizui_E_0026():
        """
        1、网络异常
        2、已登录客户端
        3、当前全局搜索页面
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page(reset_required=False)
        current_mobile().set_network_status(0)
        current_mobile().activate_app()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0026():
        current_mobile().set_network_status(6)
        current_mobile().activate_app()
        search_page = SearchPage()
        search_page.click_back_button()

    @tags('ALL', 'SMOKE', "CMCC-EMAIL")
    def test_msg_huangcaizui_E_0027(self):
        """搜索关键字"""
        key_message = '1'
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
        # 正确的顺序
        expected_order = ['搜索和通讯录联系人', '联系人', '群聊', '功能', '聊天记录', '公众号']
        # 实际顺序
        actual_order = []
        for result in search_page.search_list_iterator():
            category = search_page.determine_list_item_type(result)
            if category != 0:
                if category == 1:
                    category = '搜索和通讯录联系人'
                actual_order.append(category)
        self.assertEqual(
            expected_order,
            actual_order,
            "检查点：排序规则为：搜索和通讯录联系人>本地联系人>群聊>功能>聊天记录>公众号"
        )

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0027():
        """
        1、联网正常
        2、已登录客户端
        3、当前全局搜索页面

        测试方案：
            1.号码有1的联系人：不用在这里创建，前面的用例已经导入包含“1”的号码
            2.名称有1的群聊：使用“群聊1”
            3.内容有1的聊天记录：群聊1中发送消息“1”
            4.名字包含“1”的功能：发送邮件到登录号码的139邮箱触发“139邮箱助手”
            5.名字包含“1”的公众号：不需要制造，中国移动10886
        """
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        login_num = preconditions.make_already_in_message_page(reset_required=True)

        # 先发邮件，否则无法搜索到功能“139邮箱”
        from library.core.utils.email_helper import send_email
        send_email(login_num + '@139.com', '工作日报终稿', '更新内容！')
        # 关键字交集使用“1”
        key_message = '1'
        # 消息页
        message_page = MessagePage()
        message_page.find_message('139邮箱助手', 40)
        # 创建名称为"助手"的群
        message_page.open_contacts_page()
        contacts_page = ContactsPage()
        contacts_page.open_group_chat_list()
        group_list = GroupListPage()
        # 群聊名测试数据使用“群聊1”
        group_names = ['群聊' + key_message]
        for group_name in group_names:
            group_list.wait_for_page_load()
            group_list.click_search_input()
            group_search = GroupListSearchPage()
            group_search.input_search_keyword(group_name)
            if group_search.is_group_in_list(group_name):
                group_search.click_group(group_name)
                chat = ChatWindowPage()
                if chat.is_tips_display():
                    chat.directly_close_tips_alert()
                # 制造包含关键字的聊天记录
                chat.send_message(key_message)
                chat.click_back()
                group_search.wait_for_page_load()
                group_search.click_back()
            else:
                raise AssertionError('缺少预置测试数据：没找到群聊"{}"'.format(group_names))

        group_list.click_back()

    @staticmethod
    def tearDown_test_msg_huangcaizui_E_0027():
        search_page = SearchPage()
        search_page.click_back_button()
