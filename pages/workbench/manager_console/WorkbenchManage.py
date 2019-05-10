import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class WorkbenchManagePage(BasePage):
    """工作台管理首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '特色通讯': (MobileBy.XPATH, '//*[@text="特色通讯"]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待工作台管理首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["特色通讯"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_remove_icon_by_app_name(self, name):
        """点击某个应用的移除图标"""
        locator = (MobileBy.XPATH, '//*[@text ="%s"]/../android.view.View[1]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)