from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from library.core.BasePage import BasePage
from pages.components.Footer import FooterPage
from selenium.common.exceptions import NoSuchElementException

class MeSetContactsManagerPage(BasePage):
    """我-》设置-》联系人管理"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingManageContactActivity'

    __locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '联系人管理': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                '允许和飞信访问通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_close_or_open'),
                '已开启': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_close_or_open'),
                '显示SIM卡联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_show_sim_contact'),
                '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_show_sim_contact'),
                '开启后，“和飞信-通讯录”将显示SIM卡联系人': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/ll_contact_back': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_contact_back'),
                '通讯录备份': (MobileBy.ID, ''),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }

    @TestLogger.log()
    def wait_for_contact_upload_success(self, timeout=60, auto_accept_alerts=True):
        """等待个人名片头像加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present('已备份')
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self


    @TestLogger.log()
    def wait_for_contact_dowmload_success(self, timeout=60, auto_accept_alerts=True):
        """等待个人名片头像加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present('已恢复')
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self
