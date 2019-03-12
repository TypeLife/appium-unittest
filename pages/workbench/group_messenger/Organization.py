from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class Organization(BasePage):
    """组织架构"""
    ACTIVITY = ''

    __locators = {
        '新建短信': (MobileBy.XPATH, '//*[@text="新建短信"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '搜索框': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("添加联系人")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        els = self.get_elements(self.__class__.__locators['返回'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 返回 控件")

    @TestLogger.log()
    def input_search_message(self, message):
        """输入查找信息"""
        self.input_text(self.__class__.__locators["搜索框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

