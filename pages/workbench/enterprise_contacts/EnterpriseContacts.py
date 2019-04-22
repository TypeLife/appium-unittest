import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EnterpriseContactsPage(BasePage):
    """企业通讯录首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '企业通讯录': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_actionbar"),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '企业层级': (MobileBy.ID, "android:id/title"),
        '部门名称': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_department")
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待企业通讯录首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["企业通讯录"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_enterprise_contacts_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在企业通讯录首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["企业通讯录"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_corporate_grade(self):
        """是否存在企业层级"""
        return self._is_element_present(self.__class__.__locators['企业层级'])

    @TestLogger.log()
    def is_exist_department_name(self):
        """是否存在部门名称"""
        return self._is_element_present(self.__class__.__locators['部门名称'])
