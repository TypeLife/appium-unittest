from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetPage(BasePage):
    """群聊设置页面"""

    __locators={
        '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
    }

    @TestLogger.log()
    def click_search_chat_record(self):
        """点击 查找聊天内容"""
        self.click_element(self.__class__.__locators['查找聊天内容'])

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待进入群聊设置页面"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present('群聊设置')
            )
        except:
            message = "{}s内没有加载群聊设置页面完毕".format(timeout)
            raise AssertionError(
                message
            )
        return self