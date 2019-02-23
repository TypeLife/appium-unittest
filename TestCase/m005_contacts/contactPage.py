import unittest
import uuid
import time


from library.core.common.simcardtype import CardType
from selenium.common.exceptions import TimeoutException
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.EditContactPage import EditContactPage


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


<<<<<<< HEAD

class Contacts(TestCase):
=======
@unittest.skip("修改调试中。。。。。")
class ContactsPage(TestCase):
>>>>>>> origin/dev
    """
    模块:通讯录
    文件位置:全量测试用例/8.通讯录全量测试用例 曲新莉
    表格:8.通讯录全量测试用例 曲新莉

    """
    @staticmethod
    def setUp_test_contacts_0001():
        """
        验证通讯录页面元素
        """
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(2)


    @tags('All','CMCC')
    def test_contacts_0001(self):
        contacts = ContactsPage()
        contacts.page_should_contain_text('通讯录')
        # contacts.page_should_contain_text('+')
        # contacts.page_should_contain_text('搜索')
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
        time.sleep(2)


    @staticmethod
    def setUp_test_contacts_0015():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(2)
        # 创建联系人 测试1
        ContactsPage().click_add()
        creat_contact = CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('测试1')
        creat_contact.click_input_number()
        creat_contact.input_number('17324448506')
        creat_contact.save_contact()
        time.sleep(2)
        # 创建联系人2
        ContactDetailsPage().click_back_icon()
        ContactsPage().click_add()
        creat_contact.click_input_name()
        creat_contact.input_name('测试2')
        creat_contact.click_input_number()
        creat_contact.input_number('15570670329')
        creat_contact.save_contact()
        time.sleep(2)
        ContactDetailsPage().click_back_icon()


    @tags('All', 'CMCC')
    def test_contacts_0015(self):
        """
        已保存到本地的RCS用户的profile页
        """
        ContactsPage().click_search_box()
        # 搜索联系人:测试1
        ContactListSearchPage().input_search_keyword('测试1')
        ContactListSearchPage().click_contact('测试1')
        time.sleep(3)
        # 进入个人详情页
        # 页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.page_should_contain_text('测试1')
        detailpage.page_should_contain_text('173 2444 8506')
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
        # 点击大图 可以查看大图
        detailpage.click_avatar()
        time.sleep(2)
        detailpage.click_big_avatar()
        # 点击消息按钮,进入对话
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
        # 点击分享名片
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().input_search_keyword('测试2')
        SelectContactsPage().click_cantact_avatar()
        SelectContactsPage().click_share_card()


    @staticmethod
    def setUp_test_contacts_0016():
        """
        已保存到本地的非RCS用户的profile页
        """
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

    @tags('All', 'CMCC')
    def test_contacts_0016(self):
        ContactsPage().click_search_box()
        #搜索联系人:测试2
        ContactListSearchPage().input_search_keyword('测试2')
        ContactListSearchPage().click_contact('测试2')
        time.sleep(2)
        #进入个人详情页
        #页面包含的元素
        detailpage=ContactDetailsPage()
        detailpage.page_should_contain_text('测试2')
        detailpage.page_should_contain_text('155 7067 0329')
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
        detailpage.page_should_contain_text('邀请使用')
        #点击大图 可以查看大图
        detailpage.click_avatar()
        time.sleep(2)
        detailpage.click_big_avatar()
        #点击消息按钮,进入对话
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
        SelectContactsPage().input_search_keyword('测试1')
        SelectContactsPage().click_cantact_avatar()
        SelectContactsPage().click_share_card()


    @staticmethod
    def setUp_test_contacts_0017():
        """
        已保存到本地的本机用户的profile页
        """
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        time.sleep(3)
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()

        # 创建联系人本机
        ContactsPage().click_add()
        creat_contact2=CreateContactPage()
        creat_contact2.click_input_name()
        creat_contact2.input_name('本机')
        creat_contact2.click_input_number()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
        creat_contact2.input_number(phone_number[0])
        creat_contact2.save_contact()
        time.sleep(2)
        ContactDetailsPage().click_back_icon()


    def test_contacts_0017(self):
        """
        已保存到本地的本机用户的profile页
        """
        ContactsPage().click_search_box()
        # 搜索联系人:本机
        ContactListSearchPage().input_search_keyword('本机')
        ContactListSearchPage().click_contact('本机')
        time.sleep(2)
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
        SelectContactsPage().input_search_keyword('测试1')
        SelectContactsPage().click_cantact_avatar()
        SelectContactsPage().click_share_card()
        #消息、电话、语音视频、视频电话、副号拨打、和飞信电话置灰，不可点击
        time.sleep(2)
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()


    @staticmethod
    def setUp_test_contacts_0036():
        """
        用户未加入任何企业
        """
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()  #收起键盘
        Preconditions.make_already_in_message_page()  #当前已在消息界面
        MessagePage().click_contacts()

    @tags('All', 'CMCC')
    def test_contacts_0036(self):
        contact=ContactsPage()
        contact.click_and_address()








