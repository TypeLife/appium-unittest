from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GrantPemissionsPage(BasePage):
    """权限列表界面"""
    ACTIVITY = 'com.android.packageinstaller/.permission.ui.GrantPermissionsActivity'

    __locators = {
        # "允许": (MobileBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
        # "拒绝": (MobileBy.ID, "com.android.packageinstaller:id/permission_deny_button"),
        '允许': (MobileBy.XPATH, "//*[contains(@text, '允许')]"),
        '拒绝': (MobileBy.XPATH, "//*[contains(@text, '拒绝')]"),
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
    def allow_contacts_permission(self, timeout=10, auto_accept_alerts=True):
        """
        赋予权限
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("允许")
            )
            self.click_element(self.__locators["允许"])
        except:
            print("没有检测到权限弹框，权限已赋予")
        return self

    @TestLogger.log()
    def deny_contacts_permission(self, timeout=10, auto_accept_alerts=True):
        """
        拒绝权限
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("拒绝")
            )
            self.click_element(self.__locators["拒绝"])
            self.click_element(self.__locators["取消"])
        except:
            print("没有检测到权限弹框，请检差权限配置")
        return self
