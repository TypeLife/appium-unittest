from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class FooterPage(BasePage):
    """主页页脚标签栏"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
    }

    @TestLogger.log()
    def open_me_page(self):
        """切换到标签页：我"""
        self.click_element(self.__locators['我'])

    @TestLogger.log()
    def open_message_page(self):
        """切换到标签页：消息"""
        self.click_element(self.__locators['消息'])

    @TestLogger.log()
    def open_call_page(self):
        """切换到标签页：通话"""
        self.click_element(self.__locators['通话'])

    @TestLogger.log()
    def open_workbench_page(self):
        """切换到标签页：工作台"""
        self.click_element(self.__locators['工作台'])

    @TestLogger.log()
    def open_contacts_page(self):
        """切换到标签页：通讯录"""
        self.click_element(self.__locators['通讯录'])
