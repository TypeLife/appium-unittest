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
                'com.chinasofti.rcs:id/setting_simplified_chinese_img': (
                MobileBy.ID, 'com.chinasofti.rcs:id/setting_simplified_chinese_img'),
                '繁體中文(香港)': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_traditional_chinese_img'),
                'com.chinasofti.rcs:id/setting_traditional_chinese_img': (
                MobileBy.ID, 'com.chinasofti.rcs:id/setting_traditional_chinese_img'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
