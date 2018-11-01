import re
import unittest
import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SmsLoginPage(BasePage):
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.SmsLoginActivity'

    locators = {
        "输入本机号码": (MobileBy.ID, 'com.chinasofti.rcs:id/edt_phone_number'),
        "输入验证码": (MobileBy.ID, 'com.chinasofti.rcs:id/edt_verify_sms'),
        "获取验证码": (MobileBy.ID, 'com.chinasofti.rcs:id/get_sms'),
        "登录": (MobileBy.ID, 'com.chinasofti.rcs:id/btnLogin'),
        "已阅读并同意": (MobileBy.ID, 'com.chinasofti.rcs:id/agreement_checkbox'),
        "我知道了": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_know'),

    }

    @TestLogger.log()
    def input_phone_number(self, phone_number):
        """输入电话号码"""
        self.input_text(self.__class__.locators["输入本机号码"], phone_number)
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
            self.click_element(self.__class__.locators["获取验证码"])
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
            self.click_element(self.__class__.locators["获取验证码"])
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
        self.click_element(self.__class__.locators["获取验证码"])

    @TestLogger.log()
    def input_verification_code(self, code):
        """输入验证码"""
        self.input_text(self.locators['输入验证码'], code)

    @TestLogger.log()
    def click_login(self):
        """点击登录"""
        try:
            self.wait_until(
                condition=lambda d: self._is_clickable(self.locators['登录'])
            )
        except TimeoutError:
            raise AssertionError("登录按钮没有变成可点击状态")
        try:
            self.driver.hide_keyboard()
        except:
            pass
        self.click_element(self.locators['登录'])

    @TestLogger.log()
    def click_i_know(self):
        """点击弹出框我知道了"""
        try:
            self.wait_until(
                condition=lambda d: self.page_should_contain_element(self.locators['我知道了'])
            )
        except TimeoutError:
            raise AssertionError('弹出框按钮“我知道了”没有在页面出现')
        self.click_element(self.locators['我知道了'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待短信登录页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.locators["输入本机号码"])
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
                condition=lambda d: self._is_text_present("登录验证")
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
                condition=lambda d: self._is_text_present("我知道了")
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
        self.click_element(self.__class__.locators["获取验证码"])
        time.sleep(35)
        # self.wait_for_verify_code_load()
        # 打开通知栏，通过通知栏获取验证码
        self.driver.open_notifications()
        # 获取验证码
        el = self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("登录验证")')
        code = re.findall('\d{3,8}', el.text)
        # 通知栏回退
        self.driver.back()
        return code
