from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeSetMultiLanguagePage(BasePage):
    """我-》设置-》多语言"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.MultiLanguageSettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/title_bar': (MobileBy.ID, 'com.chinasofti.rcs:id/title_bar'),
                'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                '设置语言': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                '完成': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send'),
                '简体中文': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_simplified_chinese_img'),
                '选择简体中文': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/setting_simplified_chinese_img'),
                '繁體中文(香港)': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_traditional_chinese_img'),
                '选择繁體中文(香港)': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/setting_traditional_chinese_img'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }

    @TestLogger.log()
    def select_simplified_chinese(self):
        """选择简体中文"""
        self.click_element(self.locators["选择简体中文"])

    @TestLogger.log()
    def select_traditional_chinese(self):
        """选择繁體中文(香港)"""
        self.click_element(self.locators["选择繁體中文(香港)"])

    @TestLogger.log()
    def click_finish(self):
        """点击完成"""
        self.click_element(self.locators["完成"])

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待设置语言页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present('设置语言')
            )
        except:
            message = "设置语言页面在限定的时间：{}s内没有加载完毕，或者没有包含文本：设置语言".format(timeout)
            raise AssertionError(
                message
            )
        return self
