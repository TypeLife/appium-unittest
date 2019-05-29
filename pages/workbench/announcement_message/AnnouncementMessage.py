from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AnnouncementMessagePage(BasePage):
    """公告信息页面"""
    ACTIVITY = ''

    __locators = {
        '？': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '(2人)': (MobileBy.XPATH, '//*[@text="（2人）"]'),
        '(3人)': (MobileBy.XPATH, '//*[@text="（3人）"]'),
    }

    @TestLogger.log()
    def wait_for_page_loads(self, text="未发公告", timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present(text),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_enter_more(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['？'])

    def swipe_half_page_up(self):
        """向上滑动半页"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)

    def swipe_half_page_down(self):
        """向下滑动半页"""
        self.swipe_by_percent_on_screen(50, 30, 50, 80, 800)

    @TestLogger.log()
    def click_element_(self,text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_element_(self, text,times):
        """长按元素"""
        el=self.get_element(self.__class__.__locators[text])
        self.press(el,times)

    @TestLogger.log()
    def is_element_exit(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])


