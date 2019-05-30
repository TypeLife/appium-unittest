import preconditions
from library.core.TestCase import TestCase
from selenium.common.exceptions import TimeoutException
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from pages import *
from pages.call.mutivideo import MutiVideoPage
from pages.components.BaseChat import BaseChatPage
import time
import unittest

from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage

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
    def enter_label_grouping_chat_page(enterLabelGroupingChatPage=True):
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

    @staticmethod
    def create_he_contacts(names):
        """选择手机联系人创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name in names:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name(name)
                slc.click_sure()
                time.sleep(2)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_he_contacts2(contacts):
        """手动输入联系人创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name, number in contacts:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(4)
                osp.click_specify_element_by_name("手动输入添加")
                osp.input_contacts_name(name)
                osp.input_contacts_number(number)
                osp.click_confirm()
                time.sleep(2)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()


class CallMultipartyVideo(TestCase):
    """
    模块：通话
    文件位置：1.1.5全量
    表格：通话--消息--多方视频
    """

    # @classmethod
    # def setUpClass(cls):
    #     preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             current_mobile().hide_keyboard_if_display()
    #             Preconditions.make_already_in_call()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break
    #
    #     # 导入团队联系人
    #     fail_time2 = 0
    #     flag2 = False
    #     while fail_time2 < 5:
    #         try:
    #             Preconditions.make_already_in_call()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4", "English"]
    #             Preconditions.create_he_contacts(contact_names)
    #             contact_names2 = [("Lily", "13800138050")]
    #             Preconditions.create_he_contacts2(contact_names2)
    #             flag2 = True
    #         except:
    #             fail_time2 += 1
    #         if flag2:
    #             break
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

    @staticmethod
    def setUp_test_call_zhenyishan_0007_001():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0007_001(self):
        """未订购每月10G免流，使用移动网络发起多方视频，弹出每月10G免流特权提示窗口---普通群/企业群"""
        # 1、登录的手机号码未订购每月10G免流
        # 2、当前为移动网络连接
        # Step:1、消息模块 — 普通群/企业群 — 点击视频按钮 — 点击多方视频
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
        # CheckPoint:发起多方视频，弹出每月10G免流特权提示弹窗
        time.sleep(1)
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(3)

    @staticmethod
    def tearDown_test_call_zhenyishan_0007_001():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_zhenyishan_0007_002():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0007_002(self):
        """未订购每月10G免流，使用移动网络发起多方视频，弹出每月10G免流特权提示窗口---通话模块 — 发起视频 — 勾选2--8人 — 点击呼叫"""
        # 1、登录的手机号码未订购每月10G免流
        # 2、当前为移动网络连接
        # Step:1、通话模块 — 发起视频 — 勾选2--8人 — 点击呼叫
        cpg = CallPage()
        cpg.click_multi_party_video()
        mppg = MultiPartyVideoPage()
        mppg.select_contacts_by_number("14775970982")
        mppg.select_contacts_by_number("13800138006")
        mppg.click_tv_sure()
        # CheckPoint:发起多方视频，弹出每月10G免流特权提示弹窗
        time.sleep(1)
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(2)

    @staticmethod
    def tearDown_test_call_zhenyishan_0007_002():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_zhenyishan_0007_003():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0007_003(self):
        """未订购每月10G免流，使用移动网络发起多方视频，弹出每月10G免流特权提示窗口---通话模块 — 通话记录列表 — 点击已有多方视频记录"""
        # 1、登录的手机号码未订购每月10G免流
        # 2、当前为移动网络连接
        # Step:1、通话模块 — 通话记录列表 — 点击已有多方视频记录
        self.test_call_zhenyishan_0002()
        CallPage().set_network_status(4)
        # CheckPoint:发起多方视频
        cpg = CallPage()
        cpg.click_call_history()
        # CheckPoint:发起多方视频，弹出每月10G免流特权提示弹窗
        time.sleep(1)
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android()

    @staticmethod
    def tearDown_test_call_zhenyishan_0007_003():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_zhenyishan_0007_004():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0007_004(self):
        """未订购每月10G免流，使用移动网络发起多方视频，弹出每月10G免流特权提示窗口---通话模块 — 通话记录列表 — 点击已有多方视频记录右侧的“！”进入通话详情页 — 点击再次呼叫"""
        # 1、登录的手机号码未订购每月10G免流
        # 2、当前为移动网络连接
        # Step:1、通话模块 — 通话记录列表 — 点击已有多方视频记录右侧的“！”进入通话详情页 — 点击再次呼叫
        self.test_call_zhenyishan_0002()
        CallPage().set_network_status(4)
        cpg = CallPage()
        cpg.click_call_time()
        mppg = MultiPartyVideoPage()
        mppg.click_call_again()
        # CheckPoint:发起多方视频，弹出每月10G免流特权提示弹窗
        time.sleep(1)
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(2)

    @staticmethod
    def tearDown_test_call_zhenyishan_0007_004():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_zhenyishan_0007_005():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0007_005(self):
        """未订购每月10G免流，使用移动网络发起多方视频，弹出每月10G免流特权提示窗口---通讯录模块 — 标签分组 — 点击已新建分组 — 点击多方视频"""
        # 1、登录的手机号码未订购每月10G免流
        # 2、当前为移动网络连接
        # Step:1、通讯录模块 — 标签分组 — 点击已新建分组 — 点击多方视频
        cpg = CallPage()
        Preconditions.enter_label_grouping_chat_page(False)
        LableGroupDetailPage().click_multiparty_videos()
        mppg = MultiPartyVideoPage()
        time.sleep(1)
        for i in range(3):
            mppg.click_select_contacts(i)
        mppg.click_tv_sure()
        # CheckPoint:发起多方视频，弹出每月10G免流特权提示弹窗
        time.sleep(1)
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(4)

    @staticmethod
    def tearDown_test_call_zhenyishan_0007_005():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_zhenyishan_0007_006():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0007_006(self):
        """未订购每月10G免流，使用移动网络发起多方视频，弹出每月10G免流特权提示窗口---通讯录模块—标签分组—点击已新建分组—群发消息—点击多方视频"""
        # 1、登录的手机号码未订购每月10G免流
        # 2、当前为移动网络连接
        # Step:1、通讯录模块—标签分组—点击已新建分组—群发消息—点击多方视频
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
        # CheckPoint:发起多方视频，弹出每月10G免流特权提示弹窗
        time.sleep(1)
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(5)

    @staticmethod
    def tearDown_test_call_zhenyishan_0007_006():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0038(self):
        """普通群聊：多方视频联系人选择器搜索非群成员，检查页面显示"""
        # 1、已通过群聊进入多方视频联系人选择器
        # Step:1、在搜索框输入非群成员名称
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
        gpg = GroupListPage()
        gpg.click_mult_call_icon()
        CallPage().click_mutil_video_call()
        time.sleep(1)
        SelectContactsPage().search("13800138001")
        # CheckPoint:1、页面显示“无搜索结果”
        cpg.page_should_contain_text("无搜索结果")
        cpg.click_back_by_android(3)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0039(self):
        """普通群聊：多方视频联系人选择器搜索群成员"""
        # 1、已通过群聊进入多方视频联系人选择器
        # Step:1、在搜索框输入群成员名称
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
        gpg = GroupListPage()
        gpg.click_mult_call_icon()
        CallPage().click_mutil_video_call()
        time.sleep(1)
        SelectContactsPage().search("我")
        time.sleep(1)
        # CheckPoint:1、根据输入条件，搜索出群成员
        cpg.page_should_contain_text("我")
        # CheckPoint:2、搜索结果中，已匹配的内容高亮显示
        # CheckPoint:3、点击可选中，并且清空输入内容
        mppg = MultiPartyVideoPage()
        mppg.click_contact_icon(0)
        time.sleep(1)
        cpg.page_should_contain_text("搜索成员")
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0053(self):
        """从群聊发起多方视频，在多方视频管理界面点击“+”进入联系人选择页"""
        # Step:1、从群聊发起多方视频
        # Step:2、在多方视频管理界面点击“+”进入联系人选择页
        # Step:3、检查联系人选择器
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
        time.sleep(1)
        if cpg.is_text_present("现在去开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        self.assertTrue(mppg.is_exist_end_video_call())
        # CheckPoint:1、展示群成员列表
        MutiVideoPage().click_multi_video_add_person()
        cpg.page_should_contain_text(phone_number)
        cpg.click_back_by_android()
        if mppg.is_exist_end_video_call():
            mppg.click_end_video_call()
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0057(self):
        """通话模块：搜索栏--通过简/繁体中文搜索出结果"""
        # 1、当前为多方视频联系人选择页
        # 2、本地联系人中已有简体中文名称的联系人以及繁体中文名称的联系人
        # Step:1、在输入框输入简体中文/繁体中文
        cpg = CallPage()
        cpg.click_multi_party_video()
        # CheckPoint:1、根据输入条件，搜索出姓名中含有对应简/繁体字的结果
        SelectContactsPage().search("测试号码")
        time.sleep(1)
        cpg.page_should_contain_text("14775970982")
        mppg = MultiPartyVideoPage()
        mppg.click_contact_icon(0)
        time.sleep(1)
        cpg.page_should_contain_text("搜索或输入号码")

        # CheckPoint:2、搜索结果中，已匹配的内容高亮显示
        SelectContactsPage().search("繁體")
        time.sleep(1)
        cpg.page_should_contain_text("13800138020")
        # CheckPoint:3、点击可选中，并且清空输入内容
        mppg = MultiPartyVideoPage()
        mppg.click_contact_icon(0)
        time.sleep(1)
        cpg.page_should_contain_text("搜索或输入号码")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0058(self):
        """通话模块：搜索栏--通过英文搜索出结果"""
        # 1、当前为多方视频联系人选择页
        # 2、本地联系人中已有英文名称的联系人
        # Step:1、在输入框输入英文
        cpg = CallPage()
        cpg.click_multi_party_video()
        # CheckPoint:1、根据输入条件，搜索出姓名中含有对应英文的结果
        SelectContactsPage().search("特殊!@$")
        time.sleep(1)
        cpg.page_should_contain_text("13800138040")
        # CheckPoint: 2、搜索结果中，已匹配的内容高亮显示
        # CheckPoint: 3、点击可选中，并且清空输入内容
        mppg = MultiPartyVideoPage()
        mppg.click_contact_icon(0)
        time.sleep(1)
        cpg.page_should_contain_text("搜索或输入号码")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0059(self):
        """通话模块：搜索栏--通过数字搜索出结果"""
        # 1、当前为多方视频联系人选择页
        # 2、本地联系人中已有名称含有数字的联系人
        # Step:1、在输入框输入数字
        cpg = CallPage()
        cpg.click_multi_party_video()
        # CheckPoint:1、根据输入条件，搜索出姓名、手机号码中含有对应数字的结果
        SelectContactsPage().search("大佬1")
        time.sleep(1)
        cpg.page_should_contain_text("13800138005")
        # CheckPoint: 2、搜索结果中，已匹配的内容高亮显示
        # CheckPoint: 3、点击可选中，并且清空输入内容
        mppg = MultiPartyVideoPage()
        mppg.click_contact_icon(0)
        time.sleep(1)
        cpg.page_should_contain_text("搜索或输入号码")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0060(self):
        """通话模块：搜索栏--通过数字搜索出结果"""
        # 1、当前为多方视频联系人选择页
        # 2、本地联系人中已有名称含有数字的联系人
        # Step:1、在输入框输入数字
        cpg = CallPage()
        cpg.click_multi_party_video()
        # CheckPoint:1、根据输入条件，搜索出姓名、手机号码中含有对应数字的结果
        SelectContactsPage().search("大佬1")
        time.sleep(1)
        cpg.page_should_contain_text("13800138005")
        # CheckPoint: 2、搜索结果中，已匹配的内容高亮显示
        # CheckPoint: 3、点击可选中，并且清空输入内容
        mppg = MultiPartyVideoPage()
        mppg.click_contact_icon(0)
        time.sleep(1)
        cpg.page_should_contain_text("搜索或输入号码")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0071(self):
        """通话模块：进入多方视频联系人选择页，搜索出结果，搜索栏下方显示：【放大镜图标】搜索团队联系人：【搜索内容】     >，点击跳转到团队联系人搜索结果页面"""
        # 1、当前为多方视频联系人选择页
        # Step: 1、在输入框输入任意内容
        cpg = CallPage()
        cpg.click_multi_party_video()
        # Step: 2、检查输入框下方
        SelectContactsPage().search("大佬1")
        time.sleep(1)
        # CheckPoint:1、搜索栏下方显示：【放大镜图标】搜索团队联系人：【搜索内容】
        # CheckPoint: 2、搜索超长内容时，后面...显示
        cpg.page_should_contain_text("搜索团队联系人 : 大佬1")
        # CheckPoint: 3、点击跳转到团队联系人搜索结果页面
        SelectContactsPage().click_search_he_contact()
        time.sleep(1)
        cpg.page_should_contain_text("团队联系人")
        cpg.click_back_by_android(3)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0073(self):
        """通话模块：进入多方视频联系人选择页，检查【选择团队联系人】入口"""
        # 1、当前为多方视频联系人选择页
        # 2、用户已加入企业
        # Step: 1、点击【选择团队联系人】
        cpg = CallPage()
        cpg.click_multi_party_video()
        # CheckPoint:1、跳转团队联系人选择页
        SelectContactsPage().click_search_he_contact()
        time.sleep(1)
        cpg.page_should_contain_text("选择联系人")
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_zhenyishan_0076(self):
        """通话模块：检查团队联系人选择页的页面显示"""
        # 1、当前为团队联系人选择页
        # Step: 1、检查页面显示
        cpg = CallPage()
        cpg.click_multi_party_video()
        SelectContactsPage().click_search_he_contact()
        time.sleep(1)
        # CheckPoint:1、返回按钮
        mppg = MultiPartyVideoPage()
        self.assertTrue(mppg.is_exist_back_button())

        # CheckPoint:2、标题：选择联系人
        cpg.page_should_contain_text("选择联系人")

        # CheckPoint:3、搜索栏内置灰显示“搜索或输入手机号”
        cpg.page_should_contain_text("搜索或输入手机号")

        # CheckPoint:4、呼叫按钮，置灰显示
        # CheckPoint:5、企业层级显示
        self.assertFalse(mppg.is_enabled_tv_sure())
