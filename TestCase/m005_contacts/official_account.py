import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts import OfficialAccountPage, SearchOfficialAccountPage
import time
REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
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


class OfficialAccountTest(TestCase):
    """通讯录 - 公众号模块"""

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_OfficialAccount_0001(self):
        """公众号列表为空"""
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()

        official_account = OfficialAccountPage()
        official_account.click_tag('企业号')
        official_account.assert_enterprise_account_list_is_empty()

    def setUp_test_Conts_OfficialAccount_0001(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @unittest.skip('脚本无法操作搜索公众号页面')
    def test_Conts_OfficialAccount_0002(self):
        """公众号列表为空"""
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()

        official_account = OfficialAccountPage()
        official_account.click_tag('订阅/服务号')
        official_account.click_add()

        search = SearchOfficialAccountPage()
        search.input_search_key('1')
        search.subscribe_first_items(12)
        print('test')

    def setUp_test_Conts_OfficialAccount_0002(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @staticmethod
    def setUp_test_contacts_0321():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0321(self):
        """订阅号/服务号列表显示"""
        conts_page = ContactsPage()
        officea=OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        conts_page.is_text_present('和飞信')
        conts_page.is_text_present('和飞信团队')
        conts_page.is_text_present('和飞信新闻')
        conts_page.is_text_present('中国移动10086')

    @staticmethod
    def setUp_test_contacts_0323():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0323(self):
        """公众号会话页面"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.page_contain_expresssion()
        official.page_contain_send_button()
        official.page_contain_news()
        official.page_contain_setting()

    @staticmethod
    def setUp_test_contacts_0324():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0324(self):
        """公众号会话页面,查看输入框"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.page_contain_expresssion()
        official.page_contain_send_button()
        official.page_contain_news()
        official.page_contain_setting()
        official.click_input_box()
        official.page_contain_input_box()

    @staticmethod
    def setUp_test_contacts_0325():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0325(self):
        """公众号会话页面,发送信息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        official.input_message('good news')
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text('good news')

    @staticmethod
    def setUp_test_contacts_0326():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0326(self):
        """公众号会话页面，发送表情"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.click_expression()
        official.click_expression('[微笑1]')
        official.click_send_button()
        time.sleep(1)
        official.click_expression('expression_keyboard')
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text('[微笑1]')

    @staticmethod
    def setUp_test_contacts_0327():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0327(self):
        """公众号会话页面，发送表情+信息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.input_message('good news')
        official.click_expression()
        official.click_expression('[微笑1]')
        time.sleep(2)
        official.click_send_button()
        time.sleep(1)
        official.click_expression('expression_keyboard')
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text('good news')
        official.page_should_contain_text('[微笑1]')

    @staticmethod
    def setUp_test_contacts_0328():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0328(self):
        """公众号会话页面，发送长信息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        mesaage='good news'*10
        official.input_message(mesaage)
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text(mesaage)

    @staticmethod
    def setUp_test_contacts_0329():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0329(self):
        """公众号会话页面，发送长信息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        mesaage ='www.baidu.com'
        official.input_message(mesaage)
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text(mesaage)
        official.click_baidu_button()
        time.sleep(8)
        official.page_should_contain_text("百度一下")
    @staticmethod
    def tearDown_test_contacts_0329():
        # 初始化,恢复app到默认状态
        Preconditions.reset_and_relaunch_app()

    @staticmethod
    def setUp_test_contacts_0330():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()

        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0330(self):
        """公众号会话页面，发送长信息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        conts_page.set_network_status(1)
        time.sleep(2)
        official.click_input_box()
        official.input_message()
        official.click_send_button()
        time.sleep(1)
        official.page_should_contain_sendfail_element()
        conts_page.set_network_status(6)
        time.sleep(5)
        official.click_repeat_button()
        official.click_sure_button()
        time.sleep(2)
        official.page_should_not_contain_sendfail_element()


    @staticmethod
    def tearDown_test_contacts_0330():
        # 初始化,恢复app到默认状态
        conts_page = ContactsPage()
        Preconditions.reset_and_relaunch_app()
        conts_page.set_network_status(6)

    @staticmethod
    def setUp_test_contacts_0331():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()

        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_0331(self):
        """公众号会话页面，发送长信息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()
        official.click_officel_account()
        official.click_setting_button()
        official.page_contain_element('进入公众号')
        official.page_contain_element('查看历史资讯')
        official.page_contain_element('认证主体')
        official.page_contain_element('功能介绍')
        official.page_contain_element('更多')
        official.page_contain_element('公众号头像')


    @staticmethod
    def tearDown_test_contacts_0331():
        # 初始化,恢复app到默认状态
        conts_page = ContactsPage()
        Preconditions.reset_and_relaunch_app()

if __name__ == '__main__':
    unittest.main()
