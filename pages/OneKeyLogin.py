from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class OneKeyLoginPage(BasePage):
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.OneKeyLoginActivity'

    locators = {
        "电话号码": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        "一键登录": (MobileBy.ID, 'com.chinasofti.rcs:id/one_key_login'),
        "切换另一号码登录": (MobileBy.ID, "com.chinasofti.rcs:id/change_to_smslogin"),
        "已阅读并同意复选框": (MobileBy.ID, "com.chinasofti.rcs:id/agreement_checkbox")
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
