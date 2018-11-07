from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeSmsSetPage(BasePage):
    """ 我-》设置-》短信设置"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SmsSettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '短信设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                '应用内收发短信': (MobileBy.ID, ''),
                '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_sms'),
                '开启后支持在和飞信内查看、发送短信': (MobileBy.ID, ''),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
