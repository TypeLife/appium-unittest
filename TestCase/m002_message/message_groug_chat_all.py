import time
import unittest
import preconditions
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            return
        sog.click_back()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name


class MsgGroupChatTest(TestCase):
    """
    模块：消息->群聊
    文件位置：114全量测试用例-韦凤莲0322.xlsx
    表格：消息-群聊
    """

    # @classmethod
    # def setUpClass(cls):
    #     # 创建联系人
    #     fail_time = 0
    #     import dataproviders
    #     while fail_time < 3:
    #         try:
    #             # 获取需要导入的联系人数据
    #             required_contacts = dataproviders.get_preset_contacts()[:3]
    #             # 连接手机
    #             conts = ContactsPage()
    #             Preconditions.select_mobile('Android-移动')
    #             current_mobile().hide_keyboard_if_display()
    #             # 导入数据
    #             for name, number in required_contacts:
    #                 preconditions.make_already_in_message_page()
    #                 conts.open_contacts_page()
    #                 conts.create_contacts_if_not_exits(name, number)
    #             # # 创建群
    #             name_list = ['给个红包1', '给个红包2']
    #             group_name_list = ['群聊1']
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name in group_name_list:
    #                 group_list.wait_for_page_load()
    #                 group_list.create_group_chats_if_not_exits(group_name, name_list)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             return
    #         except Exception as e:
    #             fail_time += 1
    #             print(e)

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            if mess.get_top_news_name() == Preconditions.get_group_chat_name():
                mess.choose_chat_by_name(Preconditions.get_group_chat_name())
                return
            Preconditions.enter_group_chat_page()
            return
        scp = GroupChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0001(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""
        # 关闭网络发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.mobile.turn_off_mobile_data()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        group_chat_page = GroupChatPage()
        self.assertTrue(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0002(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0001()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0002():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0003(self):
        """对发送失败的文件进行重发"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0001()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            group_chat_page.click_back()  # xiugaichu
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        group_chat_page.wait_for_message_down_file()
        self.assertTrue(group_chat_page.check_message_resend_success())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0003():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0004(self):
        """对发送失败的文件进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0003()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertFalse(message_page.is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0005(self):
        """点击取消重发文件消失，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0001()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0005():
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0006(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file("2M_data.json")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0007(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file("2M_data.json")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0006()
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0009(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file("2M_data.json")
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'),
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0009():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0011(self):
        """在文件列表页选择文件后再点击取消按钮，停留在当前页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.select_file(".xlsx")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0012(self):
        """在文件列表页点击返回按钮时可正常逐步返回到会话页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.enter_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.select_file(".xlsx")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0013(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0014(self):
        """网络异常时勾选本地照片内任意相册的图片点击发送按钮"""
        # 1, 聊天页面打开文件夹
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.mobile.turn_off_mobile_data()
        chat_more.close_more()
        chat_more.click_file1()
        # 2， 选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0015(self):
        """会话页面有图片发送失败时查看消息列表是否有消息发送失败的标识"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0014()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0015():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0016(self):
        """对发送失败的图片文件进行重发"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0014()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            group_chat_page.click_back()
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        self.assertFalse(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0017(self):
        """对发送失败的图片进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0016()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0018(self):
        """点击取消重发图片消息，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0014()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0018():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0019(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_pic.jpg")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0020(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_pic.jpg")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0019()
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0022(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_pic.jpg")
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0022():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0024(self):
        """在选择图片页面选择文件后再点击取消按钮，停留在当前页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.select_file("23e.jpg")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0025(self):
        """在选择图片页面点击返回按钮时可正常逐步返回到会话页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        local_file.select_file("23e.jpg")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0027(self):
        """勾选本地视频内任意视频点击发送按钮"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0028(self):
        """网络异常时勾选本地文件内任意视频点击发送按钮"""
        # 1, 聊天页面打开文件夹
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.mobile.turn_off_mobile_data()
        chat_more.close_more()
        chat_more.click_file1()
        # 2， 选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0029(self):
        """会话页面有视频发送失败时查看消息列表是否有消息发送失败的标识"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0028()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0029():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0030(self):
        """对发送失败的视频进行重发"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0028()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            group_chat_page.click_back()
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        self.assertFalse(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0031(self):
        """对发送失败的视频进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0030()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0032(self):
        """点击取消重发视频文件消失，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0028()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            import time
            time.sleep(2)
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0032():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0033(self):
        """未订购每月10G的用户发送大于2M的视频时有弹窗提示"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_vedio.mp4")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0034(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_vedio.mp4")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0033()
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0036(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_vedio.mp4")
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'),
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0036():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0038(self):
        """在视频列表页选择文件后再点击取消按钮，停留在当前页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.select_file(".mp4")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0039(self):
        """在视频列表页点击返回按钮时可正常逐步返回到会话页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        local_file.select_file(".mp4")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0041(self):
        """勾选音乐列表页面任意音乐点击发送按钮"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("28618718.mp3")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0042(self):
        """网络异常时勾选音乐列表页面任意音乐点击发送按钮"""
        # 1, 聊天页面打开文件夹
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.mobile.turn_off_mobile_data()
        chat_more.close_more()
        chat_more.click_file1()
        # 2， 选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("28618718.mp3")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0043(self):
        """会话页面有音乐文件发送失败时查看消息列表是否有消息发送失败的标识"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0042()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0043():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0044(self):
        """对发送失败的音乐进行重发"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0042()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            group_chat_page.click_back()
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('网络连接异常'))
            group_chat_page.mobile.wait_until_not(lambda x: group_chat_page.is_text_present('连接中'))
            MessagePage().choose_chat_by_name(Preconditions.get_group_chat_name())
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_resend_confirm()
        group_chat_page.wait_for_page_load()
        self.assertFalse(group_chat_page.is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0045(self):
        """对发送失败的音乐进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_qun_0044()
        group_chat_page = GroupChatPage()
        group_chat_page.click_back()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0046(self):
        """点击取消重发音乐文件消失，停留在当前页面"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_qun_0042()
            group_chat_page.mobile.turn_on_wifi()
            group_chat_page.mobile.turn_on_mobile_data()
            import time
            time.sleep(2)
        group_chat_page.click_msg_send_failed_button()
        group_chat_page.click_multiple_selection_delete_cancel()
        group_chat_page.wait_for_page_load()
        self.assertTrue((group_chat_page.is_on_this_page()))
        group_chat_page.click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0046():
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0047(self):
        """未订购每月10G的用户发送大于2M的音乐时有弹窗提示"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_music.mp3")
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0048(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_music.mp3")
        local_file.click_send()
        self.test_msg_weifenglian_qun_0047()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0050(self):
        """点击订购免流特权后可正常返回"""
        # 关闭wifi发送文件
        chat_more = ChatMorePage()
        chat_more.mobile.turn_off_wifi()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.select_file("2M_music.mp3")
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'),
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0050():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0052(self):
        """在音乐列表页选择文件后再点击取消按钮，停留在当前页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp3")
        local_file.select_file(".mp3")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0053(self):
        """在音乐列表页点击返回按钮时可正常逐步返回到会话页面"""
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp3")
        local_file.select_file(".mp3")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        select_file_type.click_back()
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0073(self):
        """在群聊（普通群/企业群）将自己发送的文件转发到当前会话窗口"""
        # 发送一个xls文件并返回聊天页面
        chat_more = ChatMorePage()
        chat_more.close_more()
        chat_more.click_file1()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.click_preset_file_dir()
        local_file.select_file(".xlsx")
        local_file.click_send()
        GroupChatPage().wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 选择需要转发的群名
        group_name = Preconditions.get_group_chat_name()
        SelectContactsPage().select_one_recently_contact_by_name(group_name)
        SelectContactsPage().click_sure_forward()
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0074(self):
        """将自己发送的文件转发到普通群"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertFalse(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0076(self):
        """将自己发送的文件转发到普通群时失败"""
        group_chat_page = GroupChatPage()
        group_chat_page.mobile.turn_off_wifi()
        group_chat_page.mobile.turn_off_mobile_data()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发失败并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        GroupChatPage().wait_for_page_load()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0078(self):
        """将自己发送的文件转发到普通群时点击取消转发"""
        group_chat_page = GroupChatPage()
        group_chat_page.mobile.turn_off_wifi()
        group_chat_page.mobile.turn_off_mobile_data()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_cancel_forward()
        # 点击取消留在当前页面
        SelectOneGroupPage().wait_for_page_load()
        self.assertTrue(SelectOneGroupPage().is_on_this_page())
        # 返回聊天页面
        SelectOneGroupPage().click_back()
        SelectContactsPage().click_back()
        GroupChatPage().click_back()
        group_name = Preconditions.get_group_chat_name()
        MessagePage().wait_for_page_load()
        MessagePage().delete_message_record_by_name(group_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_qun_0078():
        current_mobile().turn_on_wifi()
        current_mobile().turn_on_mobile_data()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0080(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('群聊')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            SelectOneGroupPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            GroupChatPage().wait_for_page_load()
            self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0081(self):
        """将自己发送的文件转发到在搜索框输入英文字母搜索到的群"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('test')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            SelectOneGroupPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            GroupChatPage().wait_for_page_load()
            self.assertTrue(GroupChatPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_qun_0082(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的群"""
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_file1()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            group_chat_page.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('2345')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            SelectOneGroupPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            GroupChatPage().wait_for_page_load()
            self.assertTrue(GroupChatPage().is_on_this_page())
