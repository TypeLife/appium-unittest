from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GrantPemissionsPage(BasePage):
    """权限列表界面"""
    ACTIVITY = 'com.android.packageinstaller/.permission.ui.GrantPermissionsActivity'

    __locators = {
        "允许": (MobileBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
        "拒绝": (MobileBy.ID, "com.android.packageinstaller:id/permission_deny_button"),
        # '允许': (MobileBy.XPATH, "//*[contains(@text, '允许')]"),
        # '拒绝': (MobileBy.XPATH, "//*[contains(@text, '拒绝')]"),
        "取消": (MobileBy.ID, "com.chinasofti.rcs:id/btn_cancel"),
    }

    @TestLogger.log()
    def click_allow(self):
        """点击允许"""
        self.click_element(self.__locators["允许"])

    @TestLogger.log()
    def click_deny(self):
        """点击拒绝"""
        self.click_element(self.__locators["拒绝"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__locators["取消"])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在允许"""
        flag = False
        element = self.get_elements(self.__locators["允许"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def allow_contacts_permission(self):
        """赋予权限"""
        try:
            if self.is_exist_allow_button():
                self.click_element(self.__locators["允许"])
        except:
            pass

    @TestLogger.log()
    def deny_contacts_permission(self):
        """拒绝权限"""
        if self.is_exist_allow_button():
            self.click_element(self.__locators["拒绝"])
            self.click_element(self.__locators["取消"])
