from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ContactSecltorPage(BasePage):
    """多方通话选择页面"""
    ACTIVITY = 'com.cmicc.module_call.ui.activity.CalllogBannerActivity'

    __locators = {
        '选择和通讯录联系人': (MobileBy.ID, "com.chinasofti.rcs:id/text_hint"),
    }

    @TestLogger.log()
    def click_seclet_contact(self):
        """点击选择联系人"""
        self.click_element(self.__locators["选择和通讯录联系人"])

    def back(self):
        """点击返回到通话界面"""
        self.click_back()
