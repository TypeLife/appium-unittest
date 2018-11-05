from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from appium.webdriver.connectiontype import ConnectionType

class OneKeyLoginPage(BasePage):
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.OneKeyLoginActivity'

    locators = {
        "电话号码": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        "一键登录": (MobileBy.ID, 'com.chinasofti.rcs:id/one_key_login'),
        "切换另一号码登录": (MobileBy.ID, "com.chinasofti.rcs:id/change_to_smslogin"),
        "已阅读并同意复选框": (MobileBy.ID, "com.chinasofti.rcs:id/agreement_checkbox"),
        "客户端头像": (MobileBy.ID, "com.chinasofti.rcs:id/login_iron"),
        "和飞信软件许可及服务协议": (MobileBy.ID, "com.chinasofti.rcs:id/agreement_text")
    }

    @TestLogger.log()
    def assert_phone_number_equals_to(self, phone_number):
        """等待手机号读取成功"""
        self.element_text_should_be(self.__class__.locators["电话号码"], phone_number)
        return self

    @TestLogger.log()
    def click_one_key_login(self):
        """点击一键登录"""
        self.click_element(self.__class__.locators["一键登录"])

    @TestLogger.log()
    def choose_another_way_to_login(self):
        """选择验证码登录"""
        self.click_element(self.__class__.locators["切换另一号码登录"])

    @TestLogger.log()
    def check_the_agreement(self):
        """勾选我已阅读XXX协议复选框"""
        self.select_checkbox(self.__class__.locators["已阅读并同意复选框"])
        self.checkbox_should_be_selected(self.__class__.locators["已阅读并同意复选框"])
        return self

    @TestLogger.log()
    def uncheck_the_agreement(self):
        """去勾选我已阅读XXX协议复选框"""
        self.unselect_checkbox(self.__class__.locators["已阅读并同意复选框"])
        self.checkbox_should_not_be_selected(self.__class__.locators["已阅读并同意复选框"])
        return self

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待权限列表页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.element_should_be_enabled(self.__class__.locators["一键登录"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_tell_number_load(self, timeout=10, auto_accept_alerts=True):
        """等待一键登录页面的‘将以本机号码登录’变成 手机号码 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_text_present_contains(self.locators["电话号码"], r"\d+", regex=True)
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_client_logo_pic(self):
        """点击客户端头像"""
        self.click_element(self.__class__.locators["客户端头像"])

    @TestLogger.log()
    def click_license_agreement(self):
        """点击和飞信软件许可及服务协议"""
        self.click_element(self.__class__.locators["和飞信软件许可及服务协议"])
