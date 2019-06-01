import random
import time

from appium.webdriver.common.mobileby import MobileBy
from library.core.mobile.mobiledriver import MobileDriver
from library.core.mobilefactory import MobileFactory
from library.core.utils.mobilemanager import MobileManager
from mobileimplements import HuaweiP20
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *

class Preconditions(LoginPreconditions):
    """前置条件"""
    def make_contact(name):
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        #创建联系人
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        number = "147752" + str(time.time())[-5:]
        ccp.create_contact(name, number)
        ccp.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'))

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
    def setUp_test_me_zhangshuli_063():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_063(self):
        """分享我的二维码"""
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.input_search_keyword('atest')
        sc.click_element((MobileBy.XPATH,'//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @index="2"]'))
        sc.click_cancel_forward()
        sc.click_read_more()
        sc.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @index="2"]'))
        sc.click_sure_forward()

    @staticmethod
    def setUp_test_me_zhangshuli_064():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_064(self):
        """分享我的二维码"""
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)
        name = "atest" + str(random.randint(100, 999))
        Preconditions.make_contact(name)

        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.click_phone_contact()
        local_contacts_page = SelectLocalContactsPage()
        local_contacts_page.input_search_keyword("atest")
        local_contacts_page.hide_keyboard()
        # todo
        elements = local_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name"]'))
        self.assertTrue(len(elements) > 2)

    @staticmethod
    def setUp_test_me_zhangshuli_065():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_have_my_group()
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_065(self):
        """分享我的二维码"""
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.input_search_keyword("a")

        text = sc.get_text((MobileBy.ID, "com.chinasofti.rcs:id/tv_member_count"))
        self.assertTrue(lambda :(text.endswith(')') and text.startswith('(')))

    @staticmethod
    def setUp_test_me_zhangshuli_069():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_069(self):
        """分享我的二维码"""
        # Preconditions.enter_create_team_page()
        # team_name = 'team_name_' + str(random.random())[-4:];
        # Preconditions.create_team(team_name)
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.click_group_contact()
        # 选择团队联系人
        select_he_contacts_page = SelectHeContactsPage()

        select_he_contacts_page.input_search_contact_message('admin')
        select_he_contacts_page.driver.hide_keyboard()
        page = SelectContactsPage()
        page.wait_for_page_load()
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        #TODO 点击第一个联系人方法没有提供
        exist = page.is_toast_exist("该联系人不可选择")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_070():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_070(self):
        """分享我的二维码"""
        # Preconditions.enter_create_team_page()
        # team_name = 'team_name_' + str(random.random())[-4:];
        # Preconditions.create_team(team_name)
        team_name = 'admin'
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()

        sc.input_search_contact_message(team_name)
        sc.driver.hide_keyboard()
        sc.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'))
        sc.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        #TODO 点击第一个联系人方法没有提供
        exist = sc.is_toast_exist("该联系人不可选择")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_071():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_071(self):
        """分享我的二维码"""
        # Preconditions.enter_create_team_page()
        # team_name = 'team_name_' + str(random.random())[-4:];
        # Preconditions.create_team(team_name)
        team_name = 'admin'
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()

        sc.input_search_contact_message('asdasdasfewefwe')
        sc.driver.hide_keyboard()
        sc.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'))
        time.sleep(3)
        elements = sc.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/no_contact_text'))
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_me_zhangshuli_078():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_078(self):
        """分享我的二维码"""
        # Preconditions.enter_create_team_page()
        # team_name = 'team_name_' + str(random.random())[-4:];
        # Preconditions.create_team(team_name)
        team_name = 'admin'
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()

        sc.input_search_contact_message("我的电脑")
        sc.driver.hide_keyboard()
        sc.select_one_contact_by_name("我的电脑")
        sc.click_sure_forward()
        exist = sc.is_toast_exist("已转发")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_083():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_083(self):
        """和包支付--授权"""

        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))

        agreement_detail_page = AgreementDetailPage()
        match_this_page = agreement_detail_page.is_current_activity_match_this_page()
        if match_this_page :
            agreement_detail_page.click_agree_button()
        else:
            self.assertTrue(False,"没有进入授权页面")
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_me_zhangshuli_084():
        Preconditions.select_mobile('Android-移动')
        # 预制授权完成
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))

        agreement_detail_page = AgreementDetailPage()
        match_this_page = agreement_detail_page.is_current_activity_match_this_page()
        if match_this_page:
            agreement_detail_page.click_agree_button()
        agreement_detail_page.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_084(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_me_zhangshuli_088():
        Preconditions.select_mobile('Android-移动')
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))

        agreement_detail_page = AgreementDetailPage()
        match_this_page = agreement_detail_page.is_current_activity_match_this_page()
        if match_this_page:
            agreement_detail_page.click_agree_button()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_088(self):
        """和包支付--授权"""
        #TODO 卸载 安装
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))

        agreement_detail_page = AgreementDetailPage()
        match_this_page = agreement_detail_page.is_current_activity_match_this_page()
        if match_this_page:
            agreement_detail_page.click_agree_button()

    @staticmethod
    def setUp_test_me_zhangshuli_109():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_109(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        self.assertTrue(text == "0.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements :
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_me_zhangshuli_110():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_110(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        self.assertTrue(text == "1.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements :
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)
        status = agreement_detail_page.get_network_status()
        if status != 1:
            agreement_detail_page.set_network_status(1)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash_recharge'))
        exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_116():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_116(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        self.assertTrue(text == "1.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements:
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash_recharge'))

        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_tv_pass1'), '0')
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_tv_pass1'), '3')
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_tv_pass1'), '1')
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_tv_pass1'), '0')
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_tv_pass1'), '0')
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_tv_pass1'), '8')
        #输入密码的之后的xpath

    @staticmethod
    def setUp_test_me_zhangshuli_123():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_123(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        self.assertTrue(text == "0.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements:
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash_withdraw'))
        exist = agreement_detail_page.is_toast_exist("和飞信：提现金额需大于0元")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_135():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_135(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_flow_area'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_goto_charge_redpaper'))

        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/charge_content'))
        self.assertTrue(text == '可用流量不足100M，暂不能充到手机')

    @staticmethod
    def setUp_test_me_zhangshuli_136():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_136(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_flow_area'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_goto_charge_redpaper'))

        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/charge_content'))
        self.assertTrue(text == '可用流量不足100M，暂不能充到手机')
