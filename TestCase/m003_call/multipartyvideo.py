import preconditions
from library.core.TestCase import TestCase
from selenium.common.exceptions import TimeoutException
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components.BaseChat import BaseChatPage
import time
import unittest

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


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def make_already_in_call():
        """确保进入通话界面"""
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        cpg = CallPage()
        message_page = MessagePage()
        if message_page.is_on_this_page():
            cpg.click_call()
            return
        if cpg.is_on_the_call_page():
            return
        try:
            current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
        except:
            pass
        current_mobile().launch_app()
        try:
            message_page.wait_until(
                condition=lambda d: message_page.is_on_this_page(),
                timeout=15
            )
            cpg.click_call()
            return
        except TimeoutException:
            pass
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()
        cpg.click_call()

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
    def enter_label_grouping_chat_page(enterLabelGroupingChatPage = True):
        """进入标签分组会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_call()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.click_label_grouping()
        label_grouping = LabelGroupingPage()
        label_grouping.wait_for_page_load()
        # 不存在标签分组则创建
        group_name = Preconditions.get_label_grouping_name()
        group_names = label_grouping.get_label_grouping_names()
        time.sleep(1)
        if not group_names:
            label_grouping.click_new_create_group()
            label_grouping.wait_for_create_label_grouping_page_load()
            label_grouping.input_label_grouping_name(group_name)
            label_grouping.click_sure()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
            label_grouping.wait_for_page_load()
            label_grouping.select_group(group_name)
        else:
            # 选择一个标签分组
            label_grouping.select_group(group_names[0])
        lgdp = LableGroupDetailPage()
        time.sleep(1)
        # 标签分组成员小于2人，需要添加成员
        members_name = lgdp.get_members_names()
        if lgdp.is_text_present("该标签分组内暂无成员") or len(members_name) < 2:
            lgdp.click_add_members()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
        # 点击群发信息
        if enterLabelGroupingChatPage:
            lgdp.click_send_group_info()
            chat = LabelGroupingChatPage()
            chat.wait_for_page_load()

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "alg" + phone_number[-4:]
        return group_name


class CallMultipartyVideo(TestCase):
    """
    模块：通话
    文件位置：1.1.5全量
    表格：通话--消息--多方视频
    """

    # @classmethod
    # def setUpClass(cls):
    #     # 创建联系人
    #     fail_time = 0
    #     import dataproviders
    #     while fail_time < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
    #             preconditions.make_already_in_message_page()
    #             current_mobile().hide_keyboard_if_display()
    #             preconditions.make_already_in_message_page()
    #             for name, number in required_contacts:
    #                 conts.open_contacts_page()
    #                 if conts.is_text_present("显示"):
    #                     conts.click_text("不显示")
    #                 conts.create_contacts_if_not_exits(name, number)
    #
    #             # 创建群
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             return
    #         except:
    #             fail_time += 1
    #             import traceback
    #             msg = traceback.format_exc()
    #             print(msg)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     current_mobile().hide_keyboard_if_display()
    #     preconditions.make_already_in_message_page()

    def default_setUp(self):
        """进入Call页面,清空通话记录"""
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()

    # def default_tearDown(self):
    #     pass

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0001(self):
        """多方视频入口检查：群聊天窗口，wifi发起多方视频"""
        # 1、wifi连接正常
        # 2、当前为消息模块
        # Step:1、进入群聊天窗口
        cpg = CallPage()
        mp = MessagePage()
        ContactsPage().click_message_icon()
        mp.wait_for_page_load()
        mp.click_add_icon()
        mp.click_group_chat()
        # 点击选择一个群
        scg = SelectContactsPage()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sog.selecting_one_group_by_name("Test_" + phone_number)
        # Step: 2、勾选2 - 8人，点击呼叫
        gpg = GroupListPage()
        gpg.click_mult_call_icon()
        CallPage().click_mutil_video_call()
        mppg = MultiPartyVideoPage()
        for i in range(3):
            mppg.click_contact_icon(i)
        mppg.click_tv_sure()
        # CheckPoint:1.发起多方视频
        time.sleep(1)
        if cpg.is_text_present("现在去开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        mppg.click_end_video_call()
        mppg.click_btn_ok()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0002(self):
        """多方视频入口检查：通话模块一级界面，多方视频按钮，wifi发起多方视频"""
        # 1、wifi连接正常
        # 2、当前为通话模块
        # Step:1、点击发起视频
        # Step:2、勾选2-8人，点击呼叫
        cpg = CallPage()
        cpg.click_multi_party_video()
        mppg = MultiPartyVideoPage()
        mppg.select_contacts_by_number("14775970982")
        mppg.select_contacts_by_number("13800138006")
        mppg.click_tv_sure()
        # CheckPoint:发起多方视频
        time.sleep(1)
        if cpg.is_text_present("现在去开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        mppg.click_end_video_call()
        mppg.click_btn_ok()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0003(self):
        """多方视频入口检查：通话记录列表，wifi发起多方视频"""
        # 1、wifi连接正常
        # 2、通话记录列表已有多方视频记录
        # Step:1、点击多方视频通话记录
        self.test_call_zhenyishan_0002()
        # CheckPoint:发起多方视频
        cpg = CallPage()
        cpg.click_call_history()
        mppg = MultiPartyVideoPage()
        time.sleep(1)
        cpg.click_cancel_open()
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        mppg.click_end_video_call()
        mppg.click_btn_ok()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0004(self):
        """多方视频入口检查：通话记录详情页，wifi发起多方视频"""
        # 1、wifi连接正常
        # 2、通话记录
        # Step:1、点击多方视频通话记录的“！”
        # Step:2、点击再次呼叫
        # CheckPoint:发起多方视频
        self.test_call_zhenyishan_0002()
        cpg = CallPage()
        cpg.click_call_time()
        mppg = MultiPartyVideoPage()
        mppg.click_call_again()
        time.sleep(1)
        cpg.click_cancel_open()
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        mppg.click_end_video_call()
        mppg.click_btn_ok()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0005(self):
        """多方视频入口检查：标签分组，wifi发起多方视频"""
        # 1、wifi连接正常
        # 2、当前为通讯录模块
        # Step:1、进入标签分组
        # Step:2、进入任意一个分组
        # Step:3、勾选联系人，点击呼叫
        cpg = CallPage()
        Preconditions.enter_label_grouping_chat_page(False)
        LableGroupDetailPage().click_multiparty_videos()
        mppg = MultiPartyVideoPage()
        time.sleep(1)
        for i in range(3):
            mppg.click_select_contacts(i)
        mppg.click_tv_sure()
        # CheckPoint:发起多方视频
        time.sleep(1)
        cpg.click_cancel_open()
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        mppg.click_end_video_call()
        mppg.click_btn_ok()
        cpg.click_back_by_android(2)
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0006(self):
        """多方视频入口检查：标签分组-群发消息，wifi发起多方视频"""
        # 1、wifi连接正常
        # 2、当前为通讯录模块
        # Step:1、进入标签分组
        # Step:2、进入任意一个分组
        # Step:3、点击群发消息
        Preconditions.enter_label_grouping_chat_page()
        cpg = CallPage()
        # Step:4、勾选联系人，点击呼叫
        gpg = GroupListPage()
        gpg.click_mult_call_icon()
        CallPage().click_mutil_video_call()
        mppg = MultiPartyVideoPage()
        for i in range(3):
            mppg.click_contact_icon(i)
        mppg.click_tv_sure()
        time.sleep(1)
        # CheckPoint:发起多方视频
        if cpg.is_text_present("现在去开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        mppg.click_end_video_call()
        mppg.click_btn_ok()
        cpg.click_back_by_android(3)
        cpg.click_call()




