import re
import time
import unittest

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages import Agreement

REQUIRED_MOBILES = {
    "测试机": 'M960BDQN229CH',
    "辅助机": 'jlyuan',
    "移动 IOS客户端": '',
}


class Preconditions(object):
    """
    分解前置条件
    """

    @staticmethod
    def select_single_cmcc_android_4g_client():
        """
        启动
        1、4G，安卓客户端
        2、移动卡
        :return:
        """
        client = switch_to_mobile(REQUIRED_MOBILES['测试机'])
        client.connect_mobile()

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
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load()

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load()
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_for_page_load(20)

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def app_start_for_the_first_time():
        """首次启动APP（使用重置APP代替）"""
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
    def background_app(seconds):
        """后台运行"""
        current_mobile().background_app(seconds)


class LoginTest(TestCase):
    """Login 模块"""

    def setUp_test_login_0001(self):
        Preconditions.select_single_cmcc_android_4g_client()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        Preconditions.take_logout_operation_if_already_login()

    @tags('ALL')
    def test_login_0001(self, login_time=60):
        """ 本网非首次登录已设置头像-一键登录页面元素检查"""
        oklp = OneKeyLoginPage()
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 检查电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_MOBILE)
        oklp.assert_phone_number_equals_to(phone_numbers[0])
        # 检查 服务协议
        oklp.page_should_contain_text("服务条款")
        # 登录
        # oklp.check_the_agreement()
        oklp.click_one_key_login()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0002(self):
        # 1、已登录
        Preconditions.select_single_cmcc_android_4g_client()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        # 2、进入我页面（切换到后台之前不应该停留在消息页面，防止误判）
        MessagePage().open_me_page()
        MePage().wait_for_page_load()
        # 3、退出后台
        current_mobile().press_home_key()

    @tags('ALL')
    def test_login_0002(self):
        """已登录状态后，退出后台"""
        current_mobile().activate_app('com.chinasofti.rcs')
        mp = MePage()
        # 验证打开的页面是否是退出之前的界面（我 页面）
        mp.wait_for_page_load()

    @unittest.skip("IOS 还不支持")
    def test_login_C0003(self, phone_number='14775970982', login_time=60):
        """移动账号登录"""
        # TODO IOS手机还没做
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()

        MessagePage().wait_for_page_load(login_time)

    @unittest.skip("skip 测试条件是双卡")
    def test_login_C0004(self, phone_number='14775970982', login_time=60):
        """切换验证码登录"""
        # TODO 框架改动，待修复
        onekey = OneKeyLoginPage()
        onekey.wait_for_page_load()
        onekey.choose_another_way_to_login()

        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.input_phone_number(phone_number)
        result = sms.get_verification_code(60)
        self.assertIn('【登录验证】尊敬的用户', result)
        code = re.findall(r'\d+', result)
        sms.input_verification_code(code)
        sms.click_login()
        sms.click_i_know()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0006(self):
        LoginTest.open_app_first_time()
        LoginTest.enter_login_page()

    @unittest.skip("skip 本网单卡测试test_login_0006")
    def test_login_0006(self):
        """服务条款检查"""
        # TODO 框架改动，待修复
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        time.sleep(5)
        Agreement.AgreementPage().wait_for_license_agreement_load()

    def setUp_test_login_0007(self):
        LoginTest.open_app_first_time()
        LoginTest.enter_login_page()

    @unittest.skip("skip 本网单卡测试test_login_0007")
    def test_login_0007(self):
        """服务条款检查"""
        # TODO 框架改动，待修复
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        time.sleep(5)
        text = """和飞信业务是中国移动提供的通信服务，用户首次登录和飞信客户端即表示同意开通本业务，本业务不收取订购费用。如使用和飞信进行发送短信、拨打电话等功能可能会收取一定的费用。"""
        Agreement.AgreementPage().page_should_contain_text(text)

    def setUp_test_login_0009(self):
        LoginTest.open_app_first_time()
        LoginTest.enter_login_page()

    @unittest.skip("skip 本网单卡测试test_login_0009")
    def test_login_0009(self):
        """登录页面检查"""
        # TODO 框架改动，待修复
        oklp = OneKeyLoginPage()
        oklp.page_should_contain_text("语言")
        oklp.page_should_contain_text("一键登录")
        oklp.page_should_contain_text("《和飞信软件许可及服务协议》")
        oklp.page_should_contain_client_logo_pic()

    def setUp_test_login_0010(self):
        LoginTest.open_app_first_time()
        LoginTest.enter_login_page()

    @unittest.skip("skip 一移动一异网卡登录测试test_login_0010")
    def test_login_0010(self):
        """一移动一异网卡登录"""
        # TODO 框架改动，待修复
        oklp = OneKeyLoginPage()
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.page_should_contain_text("输入本机号码")
        sms.page_should_contain_text("输入验证码")
        sms.page_should_contain_text("获取验证码")
        sms.page_should_contain_text("切换另一号码登录")

    def setUp_test_login_0025(self):
        """异网账号进入登录页面"""
        LoginTest.open_app_first_time()
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡异网账户测试login_0025")
    def test_login_0025(self):
        """非首次已设置头像昵称登录短信登录页元素显示(异网单卡)"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        sl.page_should_contain_text("输入本机号码")
        sl.page_should_contain_text("输入验证码")
        sl.page_should_contain_text("获取验证码")
        self.assertEqual(sl.login_btn_is_checked(), 'false')

    def setUp_test_login_0026(self):
        """
        预置条件：
        1、异网账号(非首次登录)进入登录页面
        """
        LoginTest.open_app_not_first_time()

    @unittest.skip("skip 单卡（联通）输入验证码验证-异网用户测试login_0026")
    def test_login_0026(self, phone_number='18681151872'):
        """输入验证码验证-异网用户，正确有效的6位（断网)"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 获取网络链接状态
        network_status = sl.get_network_status()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入验证码
        sl.input_verification_code(code)
        # 断开网络连接
        sl.set_network_status(1)
        # 点击登录
        sl.click_login()
        sl.wait_for_i_know_load()
        # 点击‘我知道了’
        sl.click_i_know()
        # 网络异常提示
        code_info = sl.get_error_code_info_by_adb("com.chinasofti.rcs.*102101", timeout=40)
        self.assertIn("102101", code_info)
        # 恢复网络连接
        sl.set_network_status(network_status)

    def setUp_test_login_0027(self):
        """异网账号进入登录页面"""
        LoginTest.open_app_first_time()
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡（联通）输入验证码验证--错误的6位测试login_0027")
    def test_login_0027(self, phone_number='18681151872'):
        """输入验证码验证-错误的6位（异网用户）"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入错误验证码
        code = str(int(code[0]) + 1)
        sl.input_verification_code(code)
        # 点击登录
        sl.click_login()
        sl.wait_for_i_know_load()
        # 点击‘我知道了’
        sl.click_i_know()
        # 获取异常提示
        code_info = sl.get_error_code_info_by_adb("com.chinasofti.rcs.*103108", timeout=40)
        self.assertIn("103108", code_info)

    def setUp_test_login_0029(self):
        """异网账号进入登录页面"""
        LoginTest.open_app_first_time()
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡（联通）输入验证码验证--正确失效的6位验证码login_0029")
    def test_login_0029(self, phone_number='18681151872'):
        """输入验证码验证-（异网）正确失效的6位验证码"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入失效的验证码
        time.sleep(300)
        sl.input_verification_code(code[0])
        # 点击登录
        sl.click_login()
        sl.wait_for_i_know_load()
        # 点击‘我知道了’
        sl.click_i_know()
        # 获取异常提示
        code_info = sl.get_error_code_info_by_adb("com.chinasofti.rcs.*103108", timeout=40)
        self.assertIn("103108", code_info)

    def setUp_test_login_0050(self):
        """
        预置条件：
        1、异网账号进入登录页面
        """
        LoginTest.open_app_first_time()
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡异网账户测试login_0050")
    def test_login_0050(self, phone_number='18681151872', login_time=60):
        """短信验证码登录-（联通）异网用户首次登录"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入验证码，点击登录
        sl.input_verification_code(code)
        sl.click_login()
        sl.wait_for_i_know_load()
        # 点击‘我知道了’
        sl.click_i_know()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0051(self):
        """
        预置条件：
        1、异网账号(非首次登录)进入登录页面
        """
        LoginTest.open_app_not_first_time()

    @unittest.skip("skip 单卡异网账户测试login_0051")
    def test_login_0051(self, phone_number='18681151872', login_time=60):
        """短信验证码登录-异网用户登录（非首次)"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入验证码，点击登录
        sl.input_verification_code(code)
        sl.click_login()
        sl.wait_for_i_know_load()
        # 点击‘我知道了’
        sl.click_i_know()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0052(self):
        """
        预置条件：
        1、异网账号进入登录页面
        """
        LoginTest.open_app_first_time()
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡异网账户测试login_0052")
    def test_login_0052(self, phone_number='18681151872'):
        """短信验证码登录-异网不显示一键登录入口"""
        # TODO 框架改动，待修复
        sl = SmsLoginPage()
        # 输入电话号码
        sl.input_phone_number(phone_number)
        sl.page_should_not_contain_text("一键登录")


if __name__ == '__main__':
    pass
