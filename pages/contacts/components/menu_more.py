from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MenuMore(BasePage):
    """公众号更多菜单"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountDetailActivity'

    __locators = {
        '点击空白': (MobileBy.ID, 'com.chinasofti.rcs:id/touch_outside'),
        '清空消息': (MobileBy.ID, 'com.chinasofti.rcs:id/clear_msg'),
        '取消关注': (MobileBy.ID, 'com.chinasofti.rcs:id/unsubscribe'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
    }

    @TestLogger.log('点击空白')
    def click_outside_to_close_more_menu(self):
        self.click_element(self.__locators['点击空白'])

    @TestLogger.log('点击清空消息')
    def click_clean_msg_menu(self):
        self.click_element(self.__locators['清空消息'])

    @TestLogger.log('点击取消关注')
    def click_unsubscribe_menu(self):
        self.click_element(self.__locators['取消关注'])

    @TestLogger.log('判断是否显示“取消关注”菜单')
    def is_unsubscribe_menu_display(self):
        return self._is_element_present(self.__locators['取消关注'])

    @TestLogger.log('点击取消')
    def click_not_clear(self):
        self.click_element(self.__locators['取消'])

    @TestLogger.log('点击确定')
    def click_sure_clear(self):
        self.click_element(self.__locators['确定'])
