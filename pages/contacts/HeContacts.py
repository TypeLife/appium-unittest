import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class HeContactsPage(BasePage):
    """和通讯录页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseHomeActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '和通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
    }


    @TestLogger.log()
    def click_back_icon(self):
        """点击返回"""
        self.click_element(self.__locators['返回'])