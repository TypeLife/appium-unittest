import unittest

import preconditions
from library.core.utils.applicationcache import current_mobile
from pages.call.Call import CallPage
from pages.components import BaseChatPage
from pages.contacts import OfficialAccountPage, SearchOfficialAccountPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
import time



class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n = n + 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def create_message_record(messages):
        """创造消息记录"""

        for title, text in messages:
            Preconditions.enter_single_chat_page(title)
            scp = SingleChatPage()
            # 输入文本信息
            scp.input_text_message(text)
            time.sleep(2)
            scp.send_text()
            scp.click_back()

    @staticmethod
    def create_contacts_by_name(name, number):
        """检查是否存在指定联系人，没有则创建"""

        mp = MessagePage()
        mp.open_contacts_page()
        ctp = ContactsPage()
        ctp.wait_for_page_load()
        ctp.click_search_box()
        cls = ContactListSearchPage()
        cls.wait_for_page_load()
        cls.input_search_keyword(name)
        time.sleep(2)
        if cls.is_exist_contacts():
            cls.click_back()
        else:
            cls.click_back()
            ctp.wait_for_page_load()
            ctp.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            ccp.input_name(name)
            time.sleep(2)
            ccp.input_number(number)
            ccp.save_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back_icon()
        ctp.wait_for_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

class MessageListTotalQuantityTest(TestCase):
    """
    模块：消息列表
    文件位置：1.1.3全量测试用例->113全量用例--肖立平.xlsx
    表格：消息列表
    """

    def default_setUp(self):

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            preconditions.force_close_and_launch_app()
            mess.wait_for_page_load()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0024(self):
        """消息列表进入"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前页面不在消息列表模块
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_me_page_load()
        time.sleep(2)
        # 进入消息列表
        mp.open_message_page()
        # 1.等待消息列表页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0025(self):
        """登录之后消息列表进入"""

        # 重启客户端
        preconditions.force_close_and_launch_app()
        mp = MessagePage()
        # 1.登录客户端,等待消息列表页面加载
        mp.wait_for_page_load()
        # 2.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_enabled(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0026(self):
        """消息列表载入"""

        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        # 1.重启客户端,等待消息列表页加载,验证页面搜索,底部tab,右上角+是否可点击
        preconditions.force_close_and_launch_app()
        mp.wait_for_page_load()
        self.assertEquals(mp.search_box_is_enabled(), True)
        self.assertEquals(mp.message_icon_is_enabled(), True)
        self.assertEquals(mp.call_icon_is_enabled(), True)
        self.assertEquals(mp.workbench_icon_is_enabled(), True)
        self.assertEquals(mp.contacts_icon_is_enabled(), True)
        self.assertEquals(mp.me_icon_is_enabled(), True)
        self.assertEquals(mp.add_icon_is_enabled(), True)
        # 2.搜索框下方提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly(), True)
        # 3.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_enabled(), True)

    @staticmethod
    def tearDown_test_message_list_total_quantity_0026():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0027(self):
        """消息列表进入到会话页面"""

        mp = MessagePage()
        # 等待消息列表页加载
        mp.wait_for_page_load()
        # 确保消息列表有消息记录
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        scp = SingleChatPage()
        text = "111"
        scp.input_text_message(text)
        time.sleep(2)
        scp.send_text()
        scp.click_back()
        mp.wait_for_page_load()
        # 1.进入到会话页面
        mp.choose_chat_by_name(name)
        scp.wait_for_page_load()
        # 返回消息列表页
        scp.click_back()

    @tags('ALL', 'CMCC_RESET', 'LXD')
    def test_message_list_total_quantity_0029(self):
        """消息列表未读消息清空"""

        # 重置当前app
        current_mobile().reset_app()
        LoginPreconditions.make_already_in_one_key_login_page()
        LoginPreconditions.login_by_one_key_login()
        mp = MessagePage()
        mp.wait_for_message_list_load()
        # 确保消息列表有未读消息
        self.assertEquals(mp.is_exist_unread_messages(), True)
        # 清空未读消息
        mp.clear_up_unread_messages()
        # 1.验证未读消息小红点标识是否消失
        self.assertEquals(mp.is_exist_unread_messages(), False)

    @unittest.skip("暂时难以实现,跳过")
    def test_message_list_total_quantity_0034(self):
        """消息列表订阅号红点显示"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 切换到标签页：通讯录
        mp.open_contacts_page()
        cp = ContactsPage()
        time.sleep(2)
        # 进入公众号页面
        cp.click_official_account_icon()
        oap = OfficialAccountPage()
        oap.wait_for_page_load()
        # 进入搜索公众号页面
        oap.click_add()
        soap = SearchOfficialAccountPage()
        soap.wait_for_page_load()
        name = "移周刊"
        soap.input_search_key(name)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0038(self):
        """消息列表网络异常显示"""

        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        time.sleep(5)
        # 1.是否提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly(), True)
        # 2.等待消息页面加载
        mp.wait_for_page_load()

    @staticmethod
    def tearDown_test_message_list_total_quantity_0038():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)









