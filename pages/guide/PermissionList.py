from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PermissionListPage(BasePage):
    """权限列表页（引导页结束后会进入该页面）"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.PermissionListActivity'

    __locators = {
        "确定": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_submit'),
        "去授权": (MobileBy.XPATH, '//*[@text="去授权"]'),
    }

    @TestLogger.log()
    def click_submit_button(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def go_permission(self):
        """点击去授权"""
        self.click_element(self.__class__.__locators["去授权"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待权限列表页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["确定"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self
