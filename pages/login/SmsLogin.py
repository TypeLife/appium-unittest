import re
import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SmsLoginPage(BasePage):
    """验证码登录页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.SmsLoginActivity'

    __locators = {
        "输入本机号码": (MobileBy.ID, 'com.chinasofti.rcs:id/edt_phone_number'),
        "输入验证码": (MobileBy.ID, 'com.chinasofti.rcs:id/edt_verify_sms'),
        "获取验证码": (MobileBy.ID, 'com.chinasofti.rcs:id/get_sms'),
        "登录": (MobileBy.ID, 'com.chinasofti.rcs:id/btnLogin'),
        "已阅读并同意": (MobileBy.ID, 'com.chinasofti.rcs:id/agreement_checkbox'),
        "我知道了": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_know'),
        "和飞信软件许可及服务协议": (MobileBy.ID, "com.chinasofti.rcs:id/agreement_tv"),
        "切换另一号码登录": (MobileBy.ID, "com.chinasofti.rcs:id/change_to_one"),
        '查看详情': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check_detail'),
        '语言': (MobileBy.ID, '	com.chinasofti.rcs:id/tv_language'),
    }

    @TestLogger.log()
    def input_phone_number(self, phone_number):
        """输入电话号码"""
        self.input_text(self.__class__.__locators["输入本机号码"], phone_number)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def get_verification_code(self, timeout=20):
        """获取验证码"""
        model = self._get_device_model()
        if model in ['MI 6']:
            try:
                self.execute_shell_command('logcat', '-c')
            except:
                pass
            self.click_element(self.__class__.__locators["获取验证码"])
            try:
                result = self.wait_until(
                    condition=lambda d: re.findall(r'【登录验证】尊敬的用户：\d+| 发送失败',
                                                   self.execute_shell_command('logcat', 'appium:D', '*:S', '-d')),
                    timeout=timeout,
                )
            except TimeoutError as e:
                raise AssertionError(e.__str__())
            return result[0]
        else:
            try:
                self.execute_shell_command('logcat', '-c')
            except:
                pass
            self.click_element(self.__class__.__locators["获取验证码"])
            try:
                result = self.wait_until(
                    condition=lambda d: re.findall(r'【登录验证】尊敬的用户：\d+| 发送失败',
                                                   self.execute_shell_command('logcat', 'appium:D', '*:S', '-d')),
                    timeout=timeout,
                )
            except TimeoutError as e:
                raise AssertionError(e.__str__())
            return result[0]

    @TestLogger.log()
    def click_get_code(self):
        """点击获取验证码"""
        self.click_element(self.__class__.__locators["获取验证码"])

    @TestLogger.log()
    def input_verification_code(self, code):
        """输入验证码"""
        self.input_text(self.__locators['输入验证码'], code)

    @TestLogger.log()
    def click_login(self):
        """点击登录"""
        try:
            self.wait_until(
                condition=lambda d: self._is_clickable(self.__locators['登录'])
            )
        except TimeoutError:
            raise AssertionError("登录按钮没有变成可点击状态")
        try:
            self.driver.hide_keyboard()
        except:
            pass
        self.click_element(self.__locators['登录'])

    @TestLogger.log()
    def click_i_know(self):
        """点击弹出框我知道了"""
        try:
            self.wait_until(
                condition=lambda d: self.page_should_contain_element(self.__locators['我知道了'])
            )
        except TimeoutError:
            raise AssertionError('弹出框按钮“我知道了”没有在页面出现')
        self.click_element(self.__locators['我知道了'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待短信登录页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["输入本机号码"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_verify_code_load(self, timeout=60, auto_accept_alerts=True):
        """等待短信验证码"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("登录验证")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_i_know_load(self, timeout=10, auto_accept_alerts=True):
        """等待 我知道了"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("我知道了")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_verify_code_by_notice_board(self):
        """根据通知栏获取登录验证码"""
        self.click_element(self.__class__.__locators["获取验证码"])
        time.sleep(30)
        # self.wait_for_verify_code_load()
        # 打开通知栏，通过通知栏获取验证码
        self.driver.open_notifications()
        # 获取验证码
        el = self.driver.find_elements_by_android_uiautomator('new UiSelector().textContains("登录验证")')
        code = None
        if el:
            code = re.findall('\d{3,8}', el[-1].text)
            if code:
                code = code[0]
        # 通知栏回退
        self.driver.back()
        return code

    @TestLogger.log()
    def click_license_agreement(self):
        """点击和飞信软件许可及服务协议"""
        self.click_element(self.__class__.__locators["和飞信软件许可及服务协议"])

    @TestLogger.log()
    def login_btn_is_checked(self):
        """获取登录按钮是否可点击"""
        return self.get_element(self.__class__.__locators["登录"]).get_attribute('checked')

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在短信登录页"""
        el = self.get_elements(self.__locators['输入本机号码'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_read_agreement_detail(self):
        """点击查看详情"""
        self.click_element(self.__locators['查看详情'])

    @TestLogger.log()
    def wait_for_detail_load(self, timeout=10, auto_accept_alerts=True):
        """等待 查看详情"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("查看详情")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_one_key_or_sms_login_page_load(self, timeout=20):
        def determine_login_page(d):
            if self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/one_key_login')):
                return 'one_key'
            elif self.get_elements(self.__locators['输入本机号码']):
                return 'sms'
            else:
                return False

        try:
            page_name = self.wait_until(
                condition=determine_login_page,
                timeout=timeout
            )
            return page_name
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )

    @TestLogger.log()
    def click_language(self):
        """点击查看详情"""
        self.click_element(self.__locators['语言'])