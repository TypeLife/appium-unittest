from appium.webdriver.common.mobileby import MobileBy

from selenium.common.exceptions import TimeoutException
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeMobileAccuntPage(BasePage):
    """我-》移动营业厅"""
    # ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.OutGoingCallSettingActivity'

    __locators = {'': (MobileBy.ID, ''),

                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '查询账单': (MobileBy.ID, 'com.chinasofti.rcs:id/query_bill_button'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_left_back_layout'),
                  '充话费': (MobileBy.ID, 'com.chinasofti.rcs:id/charge_call_button'),
                  }

    @TestLogger.log('点击返回')
    def click_mobile_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('点击充话费')
    def click_chargrmobile(self):
        self.click_element(self.__locators["充话费"])
