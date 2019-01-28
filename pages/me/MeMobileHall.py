from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException


class   MeMobileHallPage(BasePage):
    """我-》移动营业厅"""
    # ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.OutGoingCallSettingActivity'

    __locators = {'': (MobileBy.ID, ''),

                'android:id/content': (MobileBy.ID, 'android:id/content'),
                '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                '网上营业厅': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_title_tv'),
                '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_left_btn'),
                '账号余额': (MobileBy.ID, 'com.chinasofti.rcs:id/homebalance'),
                }

    @TestLogger.log('点击账户余额')
    def click_mobile_account(self):
        self.click_element(self.__locators["账号余额"])

    @TestLogger.log('返回网上营业厅')
    def rallbackto_mobile(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('网上营业厅是否正常打开')
    def assert_enterprise_account_list_is_empty(self):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['网上营业厅'])
            )
            self.element_text_should_be(
                self.__locators['网上营业厅'],
                '网上营业厅', '检查点：网上营业厅是否正常打开：正常打开'
            )
        except TimeoutException:
            raise AssertionError("检查点：网上营业厅不能正常打开")
