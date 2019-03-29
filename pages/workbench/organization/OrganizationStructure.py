from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class OrganizationStructurePage(BasePage):
    """组织架构首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5Activity'

    __locators = {
        '组织架构': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text ="组织架构"]'),
        '返回': (MobileBy.ID, "com.chinasofti.rcs:id/btn_back_actionbar")
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待组织架构首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["组织架构"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_exist_specify_element_by_name(self, name):
        """是否存在指定元素"""
        locator = (MobileBy.XPATH, '//*[@text="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def click_specify_element_by_name(self, name):
        """点击指定元素"""
        locator = (MobileBy.XPATH, '//*[@text="%s"]' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
