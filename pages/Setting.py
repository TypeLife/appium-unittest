from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SettingPage(BasePage):
    """设置页面"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingActivity'

    __locators = {
        '菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        'com.chinasofti.rcs:id/default_SMS_app': (MobileBy.ID, 'com.chinasofti.rcs:id/default_SMS_app'),
        'com.chinasofti.rcs:id/callControl': (MobileBy.ID, 'com.chinasofti.rcs:id/callControl'),
        '来电管理': (MobileBy.ID, 'com.chinasofti.rcs:id/incoming_call_text'),
        'com.chinasofti.rcs:id/andNumberControl': (MobileBy.ID, 'com.chinasofti.rcs:id/andNumberControl'),
        '副号管理': (MobileBy.ID, 'com.chinasofti.rcs:id/second_number_text'),
        'com.chinasofti.rcs:id/manage_contact': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_contact'),
        '联系人管理': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_contact_text'),
        'com.chinasofti.rcs:id/font_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/font_setting'),
        '字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_text'),
        'com.chinasofti.rcs:id/outgoing_call_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting'),
        '拨号设置': (MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting_text'),
        'com.chinasofti.rcs:id/multi_language_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting'),
        '多语言': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting_text'),
        'com.chinasofti.rcs:id/upload_log_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting'),
        '参与体验改善计划': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting_text'),
        'com.chinasofti.rcs:id/logout': (MobileBy.ID, 'com.chinasofti.rcs:id/logout'),
        '退出': (MobileBy.ID, 'com.chinasofti.rcs:id/login_out_text'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),

        '确定退出？': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok')
    }

    @TestLogger.log()
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['来电管理'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')

    @TestLogger.log()
    def click_logout(self):
        """点击退出"""
        self.click_element(self.__locators['退出'])

    @TestLogger.log()
    def click_ok_of_alert(self):
        """点击弹框的确定按钮"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['确定'])
        ).click()
