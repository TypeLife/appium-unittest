from pages.me.MeViewUserProfile import MeViewUserProfilePage

from pages.message.Send_CardName import Send_CardNamePage
import time

from appium.webdriver.common.mobileby import MobileBy

from pages.components import ChatNoticeDialog
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
            sog.click_back()
            return
        sog.click_back()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
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
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name

class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_login_chenjialiang_0256():
        Preconditions.select_mobile('Android-移动', True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_login_chenjialiang_0256(self):
        """登录"""
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        #消息页点击新建消息并同意权限
        message = MessagePage()
        # message.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        message.click_add_icon()
        message.click_new_message()
        message.wait_for_page_load()
        #点击返回，并判断是否正常
        message.click_back()
        self.assertTrue(message.is_on_this_page)

    @staticmethod
    def setUp_test_me_zhangshuli_019():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_019(self):
        """会话窗口中点击删除文本消息"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        time.sleep(3)
        self.assertTrue(me.is_on_this_page())
        # 打开‘查看并编辑个人资料’页面
        me.click_view_edit()
        # 点击分享名片
        view_user_profile_page = MeViewUserProfilePage()
        view_user_profile_page.page_down()
        view_user_profile_page = view_user_profile_page.click_share_card()
        # 选择本地联系人
        sc = SelectContactsPage()
        sc.click_phone_contact()
        local_contacts_page = SelectLocalContactsPage()
        search = local_contacts_page.search("1111111111111111")
        result = local_contacts_page.no_search_result()
        self.assertTrue(result)

class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_hanjiabin_0193():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0193(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        time.sleep(660)
        send_card.press_mess('给个名片2')
        mess.page_should_not_contain_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @staticmethod
    def setUp_test_msg_hanjiabin_0194():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0194(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))
        mess.page_should_not_contain_text('给个名片2')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0023():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0023(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        single.press_mess("测试一个呵呵")
        single.click_forward()
        select_page = SelectContactPage()
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        # 判断存在选择团队联系人按钮
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择一个群"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择团队联系人"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0279():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0279(self):
        """从通话——拨号盘——输入陌生号码——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在通话模块
        call = CallPage()
        # Step 1.点击拨号盘
        if not call.is_on_the_dial_pad():
            call.click_dial_pad()
        # Checkpoint 1.调起拨号盘，输入陌生号码
        call.click_one()
        call.click_three()
        call.click_seven()
        call.click_seven()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_three()
        call.click_three()
        time.sleep(3)
        # Step 2.点击上方发送消息
        call.click_send_message()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        # Checkpoint 2.进入单聊页面
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0280():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0280(self):
        call = CallPage()
        if not call.is_on_the_dial_pad():
            call.click_element((MobileBy.ID, "com.chinasofti.rcs:id/tvCall"))
        call.click_one()
        call.click_three()
        call.click_eight()
        call.click_zero()
        call.click_zero()
        call.click_one()
        call.click_three()
        call.click_eight()
        call.click_zero()
        call.click_zero()
        call.click_zero()
        time.sleep(3)
        call.click_call_profile()
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        self.assertTrue(SingleChatPage().is_on_this_page())