from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class CalllogBannerPage(BasePage):
    """多方通话引导页面"""
    ACTIVITY = 'com.cmicc.module_call.ui.activity.CalllogBannerActivity'

    __locators = {
        '多方通话': (MobileBy.ID, "com.chinasofti.rcs:id/mutil_btnFreeCall"),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_arror'),
        '知道了': (MobileBy.XPATH, "//*[contains(@text, '知道了')]"),
        '搜索或输入号码': (MobileBy.ID, "com.chinasofti.rcs:id/contact_search_bar"),
        '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
    }

    @TestLogger.log()
    def click_multiparty_call_by_calllogbanner(self):
        """点击多方通话"""
        self.click_element(self.__locators["多方通话"])

    @TestLogger.log()
    def is_on_the_calllog_banner_page(self):
        """判断当前页是否在引导页第一页"""
        time.sleep(2)
        flag = self.is_text_present("点击按钮发起电话")
        return flag

    @TestLogger.log()
    def click_i_know(self):
        """点击知道了"""
        self.click_element(self.__locators["知道了"])

    @TestLogger.log()
    def press_contact_search_bar(self):
        """长按搜索输入框"""
        el = self.get_element(self.__locators["搜索或输入号码"])
        self.press(el)

    @TestLogger.log()
    def get_contact_search_bar_text(self):
        """获取搜索输入框text"""
        return self.get_element_attribute(self, locator=self.__locators["搜索或输入号码"], attr="text", wait_time=3)

    @TestLogger.log()
    def click_copy(self):
        """点击复制"""
        self.click_element(self.__locators["复制"])

    @TestLogger.log()
    def multiparty_call(self):
        """跳过多方通话引导页面，返回到通话菜单"""
        self.click_multiparty_call_by_calllogbanner()
        self.click_i_know()
        self.click_back()
        time.sleep(1)

