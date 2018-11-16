from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetFuHaoPage(BasePage):
    """我-》设置-》副号管理"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.AndMoreNumActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                '副号管理': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_num'),
                'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                '暂未开通副号业务': (MobileBy.ID, 'com.chinasofti.rcs:id/empty_view'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
