from library.core.BasePage import BasePage
from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger


class CallPage(BasePage):
    """通话页面"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        "多方电话提示框": (MobileBy.ID, "com.chinasofti.rcs:id/mutil_btnFreeCall"),
        "返回": (MobileBy.ID, "com.chinasofti.rcs:id/back"),
        "指定提示": (MobileBy.XPATH, "//*[contains(@text, '点击按钮发起电话')]"),
        '知道了': (MobileBy.XPATH, '//*[@text="知道了"]'),
        '始终允许': (MobileBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
        "多方视频图标": (MobileBy.ID, "com.chinasofti.rcs:id/ivMultipartyVideo")
    }

    @TestLogger.log()
    def is_exist_specified_prompt(self):
        """是否存在指定提示"""
        return self._is_element_present(self.__class__.__locators["指定提示"])

    @TestLogger.log()
    def click_multi_party_telephone(self):
        """点击多方电话"""
        self.click_element(self.__class__.__locators["多方电话提示框"])

    @TestLogger.log()
    def is_exist_know(self):
        """是否存在“知道了”文本"""
        return self._is_element_present(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_know(self):
        """点击知道了"""
        self.click_element(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在始终允许"""
        return self._is_element_present(self.__class__.__locators["始终允许"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方视频图标"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self
