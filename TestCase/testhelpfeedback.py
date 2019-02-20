from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.HelpFeedBack import HelpAndFeedBackPage

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
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def app_start_for_the_first_time():
        """首次启动APP（使用重置APP代替）"""
        current_mobile().reset_app()

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
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def take_in_me_page():
        """进入“我”页面"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

    @staticmethod
    def take_in_help_page():
        """进入“帮助与反馈页面”"""
        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_help_menu()


class HelpFeedbackTest(TestCase):
    """帮助与反馈 模块"""

    @staticmethod
    def setUp_test_help_feedback_001():
        """前提条件是要进入到‘帮助与反馈’页面"""
        # 选择手机连接
        Preconditions.select_mobile('Android-移动')
        # 收起键盘
        current_mobile().hide_keyboard_if_display()
        # 重启
        Preconditions.app_start_for_the_first_time()

        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        Preconditions.take_in_me_page()
        Preconditions.take_in_help_page()

    @tags('ALL', 'CMCC','YMSDEBUG')
    def test_help_feedback_001(self):
        haf = HelpAndFeedBackPage()
        haf.wait_for_page_load()
        haf.click_question_one()
        haf.click_back()
        haf.click_question_two()
        haf.click_back()
        haf.clicl_question_three()
