import unittest
import uuid
import time


from library.core.common.simcardtype import CardType
from selenium.common.exceptions import TimeoutException
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.HeContacts import HeContactsPage
from pages.contacts.official_account import OfficialAccountPage
from pages.contacts.search_official_account import SearchOfficialAccountPage
from pages.contacts.official_account_detail import OfficialAccountDetailPage
from pages.contacts.EditContactPage import EditContactPage
from pages.contacts.components.menu_more import MenuMore


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
        one_key.wait_for_tell_number_load(60)
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
        login_num = Preconditions.login_by_one_key_login()
        return login_num


    @staticmethod
    def init_and_enter_contacts_page():
        """预置通讯录,保证开始用例之前在通讯录页面"""
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_contacts()


class ContactPage(TestCase):

    """
    模块:通讯录
    文件位置:全量测试用例/8.通讯录全量测试用例 曲新莉
    表格:8.通讯录全量测试用例 曲新莉

    """
    # @classmethod
    # def setUpClass(cls):
    #
    #     # 创建联系人
    #     fail_time = 0
    #     import dataproviders
    #     while fail_time < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             Preconditions.connect_mobile('Android-移动')
    #             current_mobile().hide_keyboard_if_display()
    #             for name, number in required_contacts:
    #                 Preconditions.make_already_in_message_page()
    #                 conts.open_contacts_page()
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


    @staticmethod
    def setUp_test_contacts_0001():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        time.sleep(1)
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(1)

    @tags('All','CMCC')
    def test_contacts_0001(self):
        """验证通讯录页面元素"""
        contacts = ContactsPage()
        contacts.page_should_contain_text('通讯录')
        # contacts.page_should_contain_element('+')
        contacts.page_should_contain_text('搜索')
        if contacts.is_text_present('备份你的手机通讯录，联系人数据不丢失'):
            contacts.page_should_contain_text('备份你的手机通讯录，联系人数据不丢失')
        time.sleep(2)
        contacts.page_should_contain_text('群聊')
        contacts.page_should_contain_text('标签分组')
        contacts.page_should_contain_text('公众号')
        contacts.page_should_contain_text('和通讯录')


    @staticmethod
    def setUp_test_contacts_0002():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()

    @tags('All', 'CMCC')
    def test_contacts_0002(self):
        """访问本地通讯录权限框,点击确定"""
        MessagePage().click_contacts()
        ContactsPage().click_always_allowed()
        time.sleep(2)


    @staticmethod
    def setUp_test_contacts_0003():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()

    @tags('All', 'CMCC')
    def test_contacts_0003(self):
        """允许访问本地通讯录"""
        MessagePage().click_contacts()
        contact=ContactsPage()
        contact.click_forbidden()
        time.sleep(1)

    @staticmethod
    def setUp_test_contacts_0015():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        time.sleep(1)
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('测试1')
        time.sleep(1)
        if ContactListSearchPage().is_contact_in_list('测试1'):
            ContactListSearchPage().click_back()
        else:
        # 创建联系人 测试1
            ContactListSearchPage().click_back()
            ContactsPage().click_add()
            creat_contact = CreateContactPage()
            creat_contact.click_input_name()
            creat_contact.input_name('测试1')
            creat_contact.click_input_number()
            creat_contact.input_number('17324448507')
            creat_contact.save_contact()
            time.sleep(2)
            ContactDetailsPage().click_back()

    @tags('All', 'CMCC')
    def test_contacts_0015(self):
        """已保存到本地的RCS用户的profile页"""
        ContactsPage().click_search_box()
        # 搜索联系人:测试1
        ContactListSearchPage().input_search_keyword('测试1')
        ContactListSearchPage().click_contact('测试1')
        time.sleep(3)
        # 进入个人详情页
        # 页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.page_should_contain_text('测试1')
        detailpage.page_should_contain_text('173 2444 8507')
        detailpage.page_should_contain_text('C')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('和飞信电话')
        detailpage.page_should_contain_text('分享名片')
        # 点击头像查看大图
        detailpage.click_avatar()
        time.sleep(2)
        detailpage.click_big_avatar()
        # 消息按钮可点击
        detailpage.click_message_icon()  # 进入消息页面
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            # 如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
            ChatWindowPage().click_back()
        else:
            ChatWindowPage().click_back()
        # 点击电话/点击语音通话/点击视频通话先不做
        # 分享名片按钮可点击
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().input_search_keyword('大佬1')
        SelectContactsPage().click_cantact_avatar()
        SelectContactsPage().click_share_card()
        #返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0016():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('All', 'CMCC')
    def test_contacts_0016(self):
        """已保存到本地的非RCS用户的profile页"""
        ContactsPage().click_search_box()
        #搜索联系人:大佬1
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        time.sleep(2)
        #进入个人详情页
        #页面包含的元素
        detailpage=ContactDetailsPage()
        detailpage.page_should_contain_text('大佬1')
        detailpage.page_should_contain_text('138 0013 8005')
        detailpage.page_should_contain_text('D')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('和飞信电话')
        detailpage.page_should_contain_text('分享名片')
        detailpage.page_should_contain_text('邀请使用')
        time.sleep(2)
        #点击头像可查看大图
        detailpage.click_avatar()
        time.sleep(2)
        detailpage.click_big_avatar()
        #消息按钮可点击
        detailpage.click_message_icon() #进入消息页面
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            #如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
            ChatWindowPage().click_back()
        else:
            ChatWindowPage().click_back()
        #点击电话/点击语音通话/点击视频通话先不做
        #点击分享名片
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().input_search_keyword('大佬2')
        SelectContactsPage().click_cantact_avatar()
        SelectContactsPage().click_share_card()
        #邀请使用按钮可点击  暂时未做

        #返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0017():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(2)
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(1)
        if ContactListSearchPage().is_contact_in_list('本机'):
            ContactListSearchPage().click_back()
        else:
        # 创建联系人 本机
            ContactListSearchPage().click_back()
            ContactsPage().click_add()
            creat_contact2 = CreateContactPage()
            creat_contact2.click_input_name()
            creat_contact2.input_name('本机')
            creat_contact2.click_input_number()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
            creat_contact2.input_number(phone_number[0])
            creat_contact2.save_contact()
            time.sleep(2)
            ContactDetailsPage().click_back_icon()

    @tags('All', 'CMCC')
    def test_contacts_0017(self):
        """已保存到本地的本机用户的profile页"""
        ContactsPage().click_search_box()
        # 搜索联系人:本机
        ContactListSearchPage().input_search_keyword('本机')
        ContactListSearchPage().click_contact('本机')
        time.sleep(5)
        # 进入个人详情页
        #判断页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.page_should_contain_text('本机')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
        detailpage.page_should_contain_text('198 4947 6421')
        detailpage.page_should_contain_text('B')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('和飞信电话')
        detailpage.page_should_contain_text('分享名片')
        #点击分享名片进入选择联系人页面，可以成功的分享给人/群
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().input_search_keyword('大佬1')
        SelectContactsPage().click_cantact_avatar()
        SelectContactsPage().click_share_card()
        #消息、电话、语音视频、视频电话、副号拨打、和飞信电话置灰，不可点击
        time.sleep(2)
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()
        time.sleep(2)
        #返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0036():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()

    @tags('All', 'CMCC')
    def test_contacts_0036(self):
        """用户未加入任何企业"""
        contact=ContactsPage()
        contact.click_and_address()
        time.sleep(3)
        HeContactsPage().page_should_contain_text('未加入企业')
        #返回通讯录页面
        HeContactsPage().click_back_icon()
        ContactsPage().click_message_icon()


    @staticmethod
    def setUp_test_contacts_0195():
        #进入通讯录页面
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_0195(self):
        """分享名片,搜索选择一个群分享名片,弹框确认是否分享"""
        ContactListSearchPage().click_share_card()
        SelectContactsPage().click_select_one_group()
        #搜索框文本显示'搜索群组'
        SelectOneGroupPage().is_text_present('搜索群组')
        #不存在搜索结果时,显示"无搜索结果
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('测试')
        SelectOneGroupPage().page_should_contain_text('无搜索结果')
        #存在搜索结果时,搜索结果包含关键字
        time.sleep(2)
        SelectOneGroupPage().click_back_icon()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('给个红包1')
        SelectOneGroupPage().is_group_in_list('给个红包1')
        SelectOneGroupPage().select_one_group_by_name('给个红包1')
        SelectOneGroupPage().click_share_business_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0196():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_0196(self):
        """群聊列表展示页面选择一个群分享"""
        ContactListSearchPage().click_share_card()
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().select_one_group_by_name('给个红包1')
        SelectOneGroupPage().is_text_present('发送名片')
        SelectOneGroupPage().click_share_business_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0197():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactDetailsPage().click_share_business_card()

    @tags('All', 'CMCC')
    def test_contacts_0197(self):
        """群聊列表展示页面选择本地联系人分享"""
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().page_should_contain_text('选择联系人')
        SelectContactsPage().page_should_contain_text('搜索或输入手机号')
        #无搜索结果时,下方是否展示：无搜索结果
        SelectContactsPage().click_search_keyword()
        SelectContactsPage().input_search_keyword('文本')
        SelectContactsPage().is_text_present('无搜索结果')
        time.sleep(2)
        #存在搜索结果时,判断显示是否正确
        SelectContactsPage().click_x_icon()
        time.sleep(1)
        SelectContactsPage().input_search_keyword('大佬2')
        SelectContactsPage().select_one_contact_by_name('大佬2')
        SelectContactsPage().click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0198():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactDetailsPage().click_share_business_card()


    # @staticmethod
    # def setUp_test_contacts_0006():
    #     """
    #     用户未加入任何企业
    #     """
    #     Preconditions.connect_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()  # 收起键盘
    #     Preconditions.make_already_in_message_page()  # 当前已在消息界面
    #     MessagePage().click_contacts()
    #
    # @tags('All', 'CMCC', "contacts")
    # def test_contacts_0006(self):
    #     contact = ContactsPage()
    #     contact.click_and_address()
    #     contact.click_search_box()
    #     contact.input_text()

    @tags('All', 'CMCC')
    def test_contacts_0198(self):
        """选择本地联系人分享名片"""
        select_contact=SelectContactsPage()
        select_contact.select_local_contacts()
        select_contact.select_one_contact_by_name('大佬2')
        time.sleep(2)
        select_contact.page_should_contain_text('发送名片')
        select_contact.click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()


    @staticmethod
    def setUp_test_contacts_0201():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().select_people_by_name('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_0201(self):
        """选择和通讯录联系人联系人分享名片"""
        SelectContactsPage().click_he_contacts()
        time.sleep(2)
        SelectContactsPage().page_should_contain_text('未加入企业')
        #选择联系人选择器页面的任意联系人
        SelectContactsPage().click_he_back()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().select_one_contact_by_name('大佬2')
        SelectContactsPage().click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()


    @staticmethod
    #和飞信联系人里面已经有超过3个已测试开始的联系人,同时有超过3个群名称包含测试字段的群组
    def setUp_test_contacts_0207():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactDetailsPage().click_share_business_card()

    @tags('All', 'CMCC')
    def test_contacts_0207(self):
        """分享名片时,搜索结果多于3人"""
        select_contacts=SelectContactsPage()
        #输入'测试'进行搜索,搜索结果显示情况
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包')
        select_contacts.hide_keyboard()
        time.sleep(2)
        select_contacts.page_should_contain_text('搜索和通讯录联系人')
        select_contacts.page_should_contain_text('本地联系人')
        select_contacts.page_should_contain_text('查看更多')
        select_contacts.page_should_contain_text('群聊')
        #选择本地联系人是否会弹出弹框 #是否弹出弹框未检测
        select_contacts.select_one_contact_by_name('给个红包1')
        select_contacts.is_text_present('发送名片')
        select_contacts.click_share_card()
        #选择群联系人是否会出现弹框  是否弹出弹框未检测
        ContactDetailsPage().click_share_business_card()
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包1')
        select_contacts.hide_keyboard()
        select_contacts.select_one_group_by_name('给个红包1')
        select_contacts.is_text_present('发送名片')
        select_contacts.click_share_card()
        #点击查看按钮,是否会展示折叠的搜索结果
        ContactDetailsPage().click_share_business_card()
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包')
        select_contacts.hide_keyboard()
        select_contacts.click_read_more()
        time.sleep(2)
        select_contacts.page_should_contain_text('给个红包4')
        select_contacts.select_one_contact_by_name('给个红包4')
        select_contacts.click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0208():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_0208(self):
        """选择最近聊天中的联系人,可分享名片"""
        select_contacts = SelectContactsPage()
        select_contacts.select_one_recently_contact_by_name('大佬2')
        time.sleep(1)
        select_contacts.page_should_contain_text('发送名片')
        select_contacts.click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0209():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_0209(self):
        """选择最近聊天中的群,可分享名片"""
        select_contacts = SelectContactsPage()
        select_contacts.select_one_recently_contact_by_name('给个红包1')
        time.sleep(1)
        select_contacts.page_should_contain_text('发送名片')
        select_contacts.click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0210():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('ALL','CMCC')
    def test_contacts_0210(self):
        """联系人选择器 搜索我的电脑"""
        time.sleep(1)
        SelectContactsPage().click_search_contact()
        SelectContactsPage().input_search_keyword('我的电脑')
        SelectContactsPage().hide_keyboard()
        time.sleep(2)
        #返回通讯录页面
        SelectContactsPage().click_back()
        ContactDetailsPage().click_back()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0211():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()


    @tags('ALL','CMCC')
    def test_contacts_0211(self):
        """联系人选择器  输入陌生手机号码"""
        time.sleep(1)
        select_contact=SelectContactsPage()
        select_contact.click_search_contact()
        select_contact.input_search_keyword('15575256658')
        select_contact.hide_keyboard()
        time.sleep(2)
        select_contact.get_element_text_net_name('未知号码')
        select_contact.get_element_text_net_number('tel:+86')
        time.sleep(2)
        #返回消息页面
        SelectContactsPage().click_back()
        ContactDetailsPage().click_back()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_0321():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('ALL', 'CMCC')
    def test_contacts_0321(self):
        "公众号默认关注公众号检查"
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        official_account = OfficialAccountPage()
        official_account.page_should_contain_text('中国移动10086')
        official_account.page_should_contain_text('和飞信')
        official_account.page_should_contain_text('和飞信团队')
        #返回通讯录页面
        official_account.click_back()


    @staticmethod
    def setUp_test_contacts_0322():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('ALL', 'CMCC')
    def test_contacts_0322(self):
        """公众号列表为空"""
        ContactsPage().click_official_account_icon()
        official_account = OfficialAccountPage()
        official_account.click_tag("企业号")
        time.sleep(1)
        official_account.page_should_contain_text('未关注任何企业号')
        official_account.assert_enterprise_account_list_is_empty()
        #返回通讯录页面
        official_account.click_back()


    @staticmethod
    def setUp_test_contacts_0323():
        #用户已关注'中软国际一家亲'公众号
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('ALL', 'CMCC')
    def test_contacts_0323(self):
        """未配置底部菜单栏的公众号"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        #公众号详情页(未配置底部菜单栏)
        official_account = OfficialAccountPage()
        time.sleep(2)
        official_account.page_should_contain_text('和飞信新闻')
        official_account.page_contain_setting()
        official_account.page_contain_input_box()
        official_account.page_contain_expresssion()
        official_account.page_contain_send_button()
        official_account.send_btn_is_clickable()
        #返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()


    @staticmethod
    def setUp_test_contacts_0324():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('ALL', 'CMCC')
    def test_contacts_0324(self):
        """已配置底部菜单栏的公众号"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信')
        #判断页面包含的元素
        official_account = OfficialAccountPage()
        time.sleep(2)
        official_account.page_should_contain_text('和飞信')
        official_account.page_contain_setting()
        official_account.page_contain_keyboard()
        official_account.page_should_contain_element_menu()
        #点击底部菜单,可以进入到菜单详情页
        official_account.click_menu_name1()
        time.sleep(1)
        official_account.page_should_contain_text('多方电话')
        official_account.click_menu_detail_name1()
        time.sleep(4)
        official_account.click_menu_detail_back()
        #点击键盘标志,页面显示输入框等
        official_account.click_keyboard()
        official_account.page_contain_input_box()
        official_account.page_contain_expresssion()
        official_account.page_contain_send_button()
        official_account.send_btn_is_clickable()
        time.sleep(2)
        #再次点击键盘,又展示底部菜单
        official_account.click_keyboard()
        official_account.page_should_contain_element_menu()
        time.sleep(2)
        #返回消息页面
        official_account.click_back()
        OfficialAccountPage().click_back()
        ContactsPage().click_message_icon()

    @staticmethod
    def setUp_test_contacts_0325():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0325(self):
        """文本消息发送成功"""
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        official_account.input_message('和飞信')
        official_account.click_send_button()
        time.sleep(2)
        official_account.page_should_contain_text('和飞信')
        #返回消息页面
        official_account.click_back()
        OfficialAccountPage().click_back()
        ContactsPage().click_message_icon()

    @staticmethod
    def setUp_test_contacts_0326():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0326(self):
        """表情符号发送成功"""
        official_account = OfficialAccountPage()
        official_account.click_expression()
        official_account.click_expression_detail()
        official_account.click_send_button()
        time.sleep(2)
        #返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0327():
        #用户已关注'中软国际一家亲'公众号
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0327(self):
        """文本消息和表情发送成功"""
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        official_account.input_message('和飞信')
        official_account.click_expression()
        official_account.click_expression_detail()
        official_account.click_send_button()
        time.sleep(2)
        #返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0328():
        #用户已关注'中软国际一家亲'公众号
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0328(self):
        """长文本消息发送成功"""
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        keyword=str("我"*255)
        official_account.input_message([keyword])
        official_account.click_send_button()
        time.sleep(2)
        #返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0329():
        #用户已关注'中软国际一家亲'公众号
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0329(self):
        """文本消息发送成功"""
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        keyword="https://www.baidu.com/"
        official_account.input_message(keyword)
        official_account.click_send_button()
        time.sleep(1)
        official_account.click_send_detail(keyword)
        time.sleep(2)
        #返回通讯录页面
        official_account.click_back()
        official_account.click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0330():
        #用户已关注'中软国际一家亲'公众号
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0330(self):
        """断网状态发送文本不成功"""
        official_account = OfficialAccountPage()
        #断网
        official_account.set_network_status(0)
        official_account.click_input_box()
        official_account.input_message('和飞信')
        official_account.click_send_button()
        time.sleep(2)
        official_account.page_should_contain_element_unsent()
        #回复网络 发送成功
        official_account.set_network_status(6)
        time.sleep(3)
        official_account.click_element_unsent()
        official_account.click_sure_resent()
        time.sleep(2)
        official_account.page_not_contain_element_unsent()
        #返回通讯录页面
        official_account.click_back()
        official_account.click_back()


    @staticmethod
    def setUp_test_contacts_0331():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信')

    @tags('ALL', 'CMCC')
    def test_contacts_0331(self):
        """公众号详情页面元素检查"""
        OfficialAccountPage().click_setting()
        time.sleep(2)
        official_account_detail=OfficialAccountDetailPage()
        official_account_detail.page_contain_public_title_name()
        official_account_detail.page_contain_public_name()
        official_account_detail.page_contain_public_header()
        official_account_detail.page_contain_public_number()
        official_account_detail.page_contain_features()
        official_account_detail.page_contain_certification()
        official_account_detail.page_should_contain_text('置顶公众号')
        official_account_detail.page_should_contain_text('查看历史资讯')
        official_account_detail.page_should_contain_text('进入公众号')
        time.sleep(2)
        #返回通讯录页面
        official_account_detail.click_back()
        OfficialAccountPage().click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0333():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0333(self):
        """公众号详情-接收消息"""
        OfficialAccountPage().click_setting()
        time.sleep(2)
        OfficialAccountDetailPage().click_to_be_top()
        #判断是否置顶  不完全
        OfficialAccountDetailPage().click_back()
        OfficialAccountPage().click_back()
        time.sleep(2)
        #返回通讯录页面
        OfficialAccountPage().click_back()


    @staticmethod
    def setUp_test_contacts_0334():
        #用户已关注'中软国际一家亲'公众号
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()


    @tags('ALL', 'CMCC')
    def test_contacts_0334(self):
        """公众号详情-查看历史资讯"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        #无历史资讯的公众号
        OfficialAccountPage().select_one_account_by_name('中软国际一家亲')
        time.sleep(1)
        OfficialAccountPage().click_setting()
        official_account_detail = OfficialAccountDetailPage()
        official_account_detail.click_read_old_message()
        time.sleep(2)
        official_account_detail.page_should_contain_text('无历史推送资讯')
        #有历史资讯时的公众号
        official_account_detail.click_back()
        official_account_detail.click_back()
        OfficialAccountPage().click_back()
        OfficialAccountPage().select_one_account_by_name('和飞信')
        time.sleep(1)
        OfficialAccountPage().click_setting()
        official_account_detail = OfficialAccountDetailPage()
        official_account_detail.click_read_old_message()
        time.sleep(5)
        official_account_detail.page_contain_time()
        #返回通讯录页面
        OfficialAccountDetailPage().click_back()
        OfficialAccountDetailPage().click_back()
        OfficialAccountPage().click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0335():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')

    @tags('ALL', 'CMCC')
    def test_contacts_0335(self):
        """公众号详情-进入公众号回话页面"""
        OfficialAccountPage().click_setting()
        time.sleep(2)
        OfficialAccountDetailPage().click_into_public()
        time.sleep(1)
        OfficialAccountPage().page_contain_setting()
        #返回通讯录页面
        OfficialAccountPage().click_back()
        OfficialAccountPage().click_back()
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0336():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信')
        time.sleep(2)
        if OfficialAccountPage().is_element_present_message():
            OfficialAccountPage().click_setting()
        else:
            OfficialAccountPage().click_keyboard()
            OfficialAccountPage().click_input_box()
            OfficialAccountPage().input_message('测试数据')
            OfficialAccountPage().click_send_button()
            time.sleep(2)
            OfficialAccountPage().click_setting()

    @tags('ALL', 'CMCC')
    def test_contacts_0336(self):
        """公众号详情-更多菜单"""
        time.sleep(2)
        official_account_detail=OfficialAccountDetailPage()
        official_account_detail.click_menu_more()
        time.sleep(1)
        #点击清空消息--取消
        menu_more=MenuMore()
        menu_more.click_clean_msg_menu()
        menu_more.click_not_clear()
        official_account_detail.click_back()
        time.sleep(2)
        OfficialAccountPage().page_contain_element_message()
        #点击清空消息--确定
        OfficialAccountPage().click_setting()
        time.sleep(1)
        official_account_detail.click_menu_more()
        menu_more.click_clean_msg_menu()
        menu_more.click_sure_clear()
        official_account_detail.click_back()
        OfficialAccountPage().page_not_contain_element_message()
        #点击取消关注
        OfficialAccountPage().click_setting()
        time.sleep(1)
        official_account_detail.click_menu_more()
        menu_more.click_unsubscribe_menu()
        time.sleep(2)
        OfficialAccountPage().is_public_in_list('和飞信')
        #返回通讯录页面
        OfficialAccountPage().click_back()

    @staticmethod
    def setUp_test_contacts_0337():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(1)

    @tags('ALL', 'CMCC')
    def test_contacts_0337(self):
        """点击+号,页面进入搜索公众号页面"""
        OfficialAccountPage().click_add()
        time.sleep(2)
        SearchOfficialAccountPage().page_should_contain_text('搜索公众号')
        #返回通讯录页面
        SearchOfficialAccountPage().click_back()
        OfficialAccountPage().click_back()


    @staticmethod
    def setUp_test_contacts_0345():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_official_account_icon()
        time.sleep(2)
        OfficialAccountPage().select_one_account_by_name('中国移动10086')
        time.sleep(2)
        if OfficialAccountPage().is_element_present_message():
            OfficialAccountPage().click_setting()
        else:
            OfficialAccountPage().click_keyboard()
            OfficialAccountPage().click_input_box()
            OfficialAccountPage().input_message('测试数据')
            OfficialAccountPage().click_send_button()
            time.sleep(2)
            OfficialAccountPage().click_setting()


    @tags('ALL', 'CMCC')
    def test_contacts_0351(self):
        """公众号详情-清空消息"""
        time.sleep(2)
        official_account_detail=OfficialAccountDetailPage()
        official_account_detail.click_menu_more()
        time.sleep(1)
        MenuMore().click_clean_msg_menu()
        MenuMore().click_sure_clear()
        official_account_detail.click_back()
        OfficialAccountPage().page_not_contain_element_message()
        #返回消息页面
        OfficialAccountPage().click_back()
        OfficialAccountPage().click_back()


#通讯录--标签分组页面
    @staticmethod
    def setUp_test_contacts_0351():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('ALL', 'CMCC')
    def test_contacts_0351(self):
        """标签分组页面元素检查"""
        ContactsPage().click_label_grouping()
        time.sleep(2)
        LabelGroupingPage().page_should_contain_text('新建分组')
        #返回通讯录页面
        LabelGroupingPage().click_back()













