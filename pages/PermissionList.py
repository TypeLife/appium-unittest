from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PermissionListPage(BasePage):
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.PermissionListActivity'

    locators = {
        "确定": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_submit'),
    }

    @TestLogger.log()
    def click_submit_button(self):
        """点击确定"""
        self.click_element(self.__class__.locators["确定"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待权限列表页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.page_should_contain_element(self.__class__.locators["确定"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self
