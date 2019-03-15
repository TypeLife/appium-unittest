from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeMobileChargePage(BasePage):
    """我-》移动营业厅"""
    # ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.OutGoingCallSettingActivity'

    __locators = {'': (MobileBy.ID, ''),

                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '18位密码': (MobileBy.ID, 'com.chinasofti.rcs:id/id_edt_password'),
                  '任意联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_select_contact'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_left_btn'),
                  '立即充值': (MobileBy.ID, 'com.chinasofti.rcs:id/id_btn_charge'),
                  }

    @TestLogger.log('立即返回')
    def click_mobile_chargesoon_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('立即充值')
    def click_mobile_chargesoon(self):
        self.click_element(self.__locators["立即充值"])

    @TestLogger.log('任意联系人')
    def click_contants_mobile(self):
        self.click_element(self.__locators["任意联系人"])

    @TestLogger.log('输入18位有效的密码')
    def input_passwod_text(self, pwd):
        # if len(pwd)==18:
        self.input_text(self.__locators["18位密码"], pwd)
    # else:
    #     raise AssertionError("please input 18 pwd "
    #                          "but did not")
    # pass
