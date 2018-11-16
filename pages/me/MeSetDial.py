from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetDialPage(BasePage):
    """我-》设置-》拨号设置"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.OutGoingCallSettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '拨号设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                'com.chinasofti.rcs:id/out_going_call_type_setting': (
                MobileBy.ID, 'com.chinasofti.rcs:id/out_going_call_type_setting'),
                '拨号方式': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_text'),
                '总是询问': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_text'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
