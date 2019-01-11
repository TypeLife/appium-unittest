import re
import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.login import Agreement

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
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
    def select_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

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
    def make_already_in_sms_login_page():
        """
        1、已经进入短信登录页
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
        permission_list.wait_for_page_load(30)
        permission_list.click_submit_button()
        page_name = one_key.wait_one_key_or_sms_login_page_load(30)
        if page_name == 'sms':
            return
        one_key.choose_another_way_to_login()
        SmsLoginPage().wait_for_page_load()

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
        message_page.wait_for_page_load(60)

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

    @staticmethod
    def diff_card_make_already_in_sms_login_page():
        """确保异网卡已在短信登录界面"""
        sms = SmsLoginPage()
        if sms.is_on_this_page():
            return
        current_mobile().reset_app()
        guide_page = GuidePage()
        guide_page.wait_until(
            lambda d: guide_page.is_text_present("解锁“免费通信”新攻略")
        )
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 确定
        PermissionListPage(). \
            wait_for_page_load(). \
            click_submit_button()
        SmsLoginPage().wait_for_page_load()

    @staticmethod
    def diff_card_enter_sms_login_page(required_mobiles_key):
        """异网卡进入短信登录界面"""
        client = switch_to_mobile(REQUIRED_MOBILES[required_mobiles_key])
        client.connect_mobile()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @staticmethod
    def diff_card_login_by_sms(card_type, login_time=60):
        """异网卡短信登录"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        phone_numbers = current_mobile().get_cards(card_type)
        # 输入电话号码
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        # 输入验证码
        sl.input_verification_code(code)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        MessagePage().wait_for_page_load(login_time)


class LoginTest(TestCase):
    """Login 模块"""

    @staticmethod
    def setUp_test_login_0001():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        Preconditions.take_logout_operation_if_already_login()

    @tags('ALL', 'CMCC')
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

    @staticmethod
    def setUp_test_login_0002():
        # 1、已登录
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        # 2、进入我页面（切换到后台之前不应该停留在消息页面，防止误判）
        MessagePage().open_me_page()
        MePage().wait_for_page_load()
        # 3、退出后台
        current_mobile().press_home_key()

    @tags('ALL', 'CMCC')
    def test_login_0002(self):
        """已登录状态后，退出后台"""
        current_mobile().activate_app('com.chinasofti.rcs')
        mp = MePage()
        # 验证打开的页面是否是退出之前的界面（我 页面）
        mp.wait_for_page_load()

    @unittest.skip("IOS先不做")
    def test_login_0003(self, phone_number='14775970982', login_time=60):
        """登录页面检查"""
        # TODO IOS手机还没做
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()

        MessagePage().wait_for_page_load(login_time)

    @staticmethod
    def setUp_test_login_0004():
        """选择安卓移动卡手机进入一键登录页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()

    @unittest.skip("存在自动化无法实现的高频点击操作")
    def test_login_0004(self):
        """登录页面检查"""
        # TODO XIN  存在自动化无法实现的高频点击操作
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        one_key.choose_another_way_to_login()

        sms = SmsLoginPage()
        sms.wait_for_page_load()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sms.input_phone_number(phone_number)
        result = sms.get_verification_code(60)
        self.assertIn('【登录验证】尊敬的用户', result)
        code = re.findall(r'\d+', result)
        sms.input_verification_code(code)
        sms.click_login()
        sms.click_i_know()
        MessagePage().wait_for_page_load(60)

    @unittest.skip("IOS用例先不做")
    def test_login_0005(self):
        """登录页面检查"""
        # TODO IOS用例先不做
        pass

    @staticmethod
    def setUp_test_login_0006():
        """选择安卓移动卡手机进入一键登录页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'CMCC')
    def test_login_0006(self):
        """服务条款检查"""
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        # 检查服务条款内容
        AgreementPage().wait_for_license_agreement_load()

    @staticmethod
    def setUp_test_login_0007():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'CMCC')
    def test_login_0007(self):
        """服务条款检查"""
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        Agreement.AgreementPage().wait_for_license_agreement_load()

    def setUp_test_login_0008(self):
        """测试机登录客户端、辅助机打开到验证码登录页"""
        # A手机已经登录
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()
        one_key = OneKeyLoginPage().wait_for_tell_number_load(60)
        self.login_number = one_key.get_login_number()
        Preconditions.login_by_one_key_login()

        # B手机进入短信登录界面
        Preconditions.select_mobile('Android-电信')
        current_mobile().reset_app()
        Preconditions.make_already_in_sms_login_page()

    @tags('ALL', '移动-电信')
    def test_login_0008(self):
        """下线提醒"""
        # 切换到辅助机2，并用测试机的号码登录
        Preconditions.select_mobile('Android-电信')
        sms_page = SmsLoginPage()
        sms_page.wait_for_page_load(30)
        sms_page.input_phone_number(self.login_number)
        # sms_page.click_get_code()

        # 切换回测试机取验证码
        mobile1 = Preconditions.select_mobile('Android-移动')
        with mobile1.listen_verification_code(120) as code:
            # 切换到手机2获取验证码
            switch_to_mobile(REQUIRED_MOBILES['Android-电信'])
            sms_page.click_get_code()
        # code = sms_page.listen_verification_code(60)

        # 切换到辅助机2
        Preconditions.select_mobile('Android-电信')
        sms_page.input_verification_code(code)
        sms_page.click_login()
        OneKeyLoginPage().click_read_agreement_detail()
        AgreementDetailPage().click_agree_button()
        sms_page.click_i_know()

        message_page = MessagePage()
        message_page.wait_for_page_load(60)

        # 切换回测试机等待下线提示
        Preconditions.select_mobile('Android-移动')
        message_page.wait_until(
            condition=lambda d: message_page.is_text_present('下线通知'),
            timeout=30
        )

    @staticmethod
    def setUp_test_login_0009():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'CMCC')
    def test_login_0009(self):
        """登录页面检查"""
        oklp = OneKeyLoginPage()
        oklp.page_should_contain_text("语言")
        oklp.page_should_contain_text("一键登录")
        oklp.page_should_contain_text("服务条款")
        oklp.page_should_contain_client_logo_pic()

    @staticmethod
    def setUp_test_login_0010():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-联通')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', '移动-联通')
    def test_login_0010(self):
        """一移动一异网卡登录"""
        oklp = OneKeyLoginPage()
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.page_should_contain_text("输入本机号码")
        sms.page_should_contain_text("输入验证码")
        sms.page_should_contain_text("获取验证码")
        sms.page_should_contain_text("切换另一号码登录")

    @staticmethod
    def setUp_test_login_0020():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-移动')
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', "移动-移动")
    def test_login_0020(self):
        """双移动卡登录"""
        oklp = OneKeyLoginPage()
        # 获取网络链接状态
        network_status = oklp.get_network_status()
        # 断开网络连接
        oklp.set_network_status(1)
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 恢复网络连接
        oklp.set_network_status(network_status)

    @staticmethod
    def setUp_test_login_0022():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-联通')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', "移动-联通")
    def test_login_0022(self):
        """一移动一异网卡登录"""
        oklp = OneKeyLoginPage()
        # 断开网络连接
        oklp.set_network_status(1)
        # 页面检查
        oklp.page_should_contain_text("语言")
        oklp.page_should_contain_text("一键登录")
        oklp.page_should_contain_text("服务条款")
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.page_should_contain_text("切换另一号码登录")
        self.assertEqual(sms.login_btn_is_checked(), 'false')
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sms.input_phone_number(phone_numbers[0])
        sms.input_verification_code(654805)
        # 点击登录
        sms.click_login()
        time.sleep(0.5)
        if sms.is_text_present("查看详情"):
            # 查看详情
            sms.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sms.is_text_present("我知道了"):
            # 点击‘我知道了’
            sms.click_i_know()
        # 网络异常提示
        flag = sms.is_toast_exist("当前网络不可用(102101)")
        self.assertTrue(flag)

    @staticmethod
    def tearDown_test_login_0022():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        oklp.set_network_status(6)

    @staticmethod
    def setUp_test_login_0023():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-移动')
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', "移动-移动")
    def test_login_0023(self):
        """双移动卡登录"""
        oklp = OneKeyLoginPage()
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)

    @staticmethod
    def setUp_test_login_0025():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0025(self):
        """非首次已设置头像昵称登录短信登录页元素显示(异网单卡)"""
        sl = SmsLoginPage()
        sl.page_should_contain_text("输入本机号码")
        sl.page_should_contain_text("输入验证码")
        sl.page_should_contain_text("获取验证码")
        self.assertEqual(sl.login_btn_is_checked(), 'false')

    @staticmethod
    def setUp_test_login_0026():
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0026(self):
        """输入验证码验证-异网用户，正确有效的6位（断网)"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入验证码
        sl.input_verification_code(code)
        # 断开网络连接
        sl.set_network_status(1)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 网络异常提示
        flag = sl.is_toast_exist("当前网络不可用(102101)")
        self.assertTrue(flag)

    @staticmethod
    def tearDown_test_login_0026():
        # 恢复网络连接
        sl = SmsLoginPage()
        sl.set_network_status(6)

    @staticmethod
    def setUp_test_login_0027():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0027(self):
        """输入验证码验证-错误的6位（异网用户）"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入错误验证码
        code = str(int(code) + 1)
        sl.input_verification_code(code)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 获取异常提示
        flag = sl.is_toast_exist("验证码有误，请重新输入(103108)")
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_login_0029():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0029(self):
        """输入验证码验证-（异网）正确失效的6位验证码"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入失效的验证码
        for i in range(60):
            xxx = sl.driver.current_activity
            time.sleep(5)
        sl.input_verification_code(code)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 获取异常提示
        flag = sl.is_toast_exist("验证码有误，请重新输入(103108)")
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_login_0036():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', '联通')
    def test_login_0036(self):
        """验证码重新获取后-（异网用户）输入之前的验证码提示"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code1 = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code1)
        time.sleep(30)
        # 第二次获取验证码
        code2 = sl.get_verify_code_by_notice_board()
        # 输入之前的验证码
        sl.input_verification_code(code1)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 获取异常提示
        flag = sl.is_toast_exist("验证码有误，请重新输入(103108)")
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_login_0047():
        Preconditions.select_mobile('Android-电信')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_sms_login_page()

    @unittest.skip('移动单卡短信登录做不了')
    def test_login_0047(self):
        """验证码获取-重新获取，输入框已输内容清空"""
        # TODO 移动单卡短信登录做不了
        pass

    @staticmethod
    def setUp_test_login_0048():
        """
        预置条件：
        1、异网账号首次进入登录页面
        """
        Preconditions.select_mobile('Android-电信')
        Preconditions.app_start_for_the_first_time()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "电信")
    def test_login_0048(self):
        """短信验证码登录-（电信）异网用户首次登录"""
        Preconditions.diff_card_login_by_sms(CardType.CHINA_TELECOM)

    @staticmethod
    def setUp_test_login_0049():
        """
        预置条件：
        1、异网账号首次进入登录页面
        """
        Preconditions.select_mobile('Android-联通')
        Preconditions.app_start_for_the_first_time()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0049(self):
        """短信验证码登录-（联通）异网用户首次登录"""
        Preconditions.diff_card_login_by_sms(CardType.CHINA_UNION)

    @staticmethod
    def setUp_test_login_0050():
        """
        预置条件：
        1、异网账号(非首次登录)进入登录页面
        """
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0050(self):
        """短信验证码登录-异网用户登录（非首次)"""
        # 登录
        Preconditions.diff_card_login_by_sms(CardType.CHINA_UNION)
        # 退出
        Preconditions.take_logout_operation_if_already_login()
        # 登录
        Preconditions.diff_card_login_by_sms(CardType.CHINA_UNION)

    @staticmethod
    def setUp_test_login_0051():
        """
        预置条件：
        1、异网账号进入登录页面
        """
        Preconditions.select_mobile('Android-联通')
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', "联通")
    def test_login_0051(self):
        """短信验证码登录-异网不显示一键登录入口"""
        sl = SmsLoginPage()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        sl.page_should_not_contain_text("一键登录")

    @staticmethod
    def setUp_test_login_0052():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'CMCC')
    def test_login_0052(self):
        """ 界面点击“语言”按钮"""
        oklp = OneKeyLoginPage()
        oklp.wait_for_page_load()
        # 点击“语言”按钮
        oklp.click_language()
        sml = MeSetMultiLanguagePage()
        # 点击繁体中文
        sml.select_traditional_chinese()
        # 点击完成
        sml.click_finish()
        # 检查繁体中文
        try:
            oklp.wait_until(
                condition=lambda d: oklp.is_text_present('一鍵登入')
            )
        except TimeoutException:
            raise AssertionError('没有找到繁体字文案：一键登录')
        # 为不影响其他用例，切换回简体中文
        oklp.click_language()
        sml.select_simplified_chinese()
        sml.click_finish()
        oklp.wait_for_page_load()


# from library.core.utils.testcasefilter import set_tags
#
# set_tags('DEBUG')
if __name__ == '__main__':
    pass
