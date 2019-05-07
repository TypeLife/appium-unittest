import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AppManagePage(BasePage):
    """应用管理首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '排序': (MobileBy.XPATH, '//*[@text="排序"]'),
        '确认': (MobileBy.XPATH, '//*[@text="确认"]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待应用管理首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["排序"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_remove_icon_by_name(self, name):
        """点击某个应用的移除图标"""
        locator = (MobileBy.XPATH, '//*[@text ="%s"]/../android.view.View[1]' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_sure(self):
        """点击确认"""
        self.click_element(self.__class__.__locators["确认"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

