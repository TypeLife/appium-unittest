from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupSMSExpensesPage(BasePage):
    """欢迎使用群短信页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'以后再说': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/chat_rich_media_vp" and @text="以后再说"]'),

}

    @TestLogger.log('以后再说')
    def click_later(self):
        """以后再说"""
        self.click_element(self.__locators['以后再说'])
