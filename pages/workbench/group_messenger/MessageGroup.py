from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MessageGroupPage(BasePage):
    """群发信使-》短信群发页面"""
    ACTIVITY = ''

    __locators = {
        '新建短信': (MobileBy.XPATH, '//*[@text="新建短信"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '收件人': (MobileBy.XPATH, '//*[@text="收件人"]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("新建短信")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_build_message(self):
        """点击新建短信"""
        els = self.get_elements(self.__class__.__locators['新建短信'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 新建短信 控件")

    @TestLogger.log()
    def click_addressee(self):
        """点击收件人"""
        els = self.get_elements(self.__class__.__locators['收件人'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 收件人 控件")

    @TestLogger.log()
    def wait_for_edit_message_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("收件人")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        els = self.get_elements(self.__class__.__locators['X'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 X 控件")