from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetCallPage(BasePage):
    """我-》设置-》来电管理"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.IncomingTelegramSettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '来电管理': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                '无信号时以wifi接听电话': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_default_wifi_call'),
                '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_default_wifi_call'),
                '当手机无信号，而和飞信客户端在线时（即有网时），来电将转为和飞信网络通话': (MobileBy.ID, ''),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
