from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetContactsManagerPage(BasePage):
    """我-》设置-》联系人管理"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingManageContactActivity'

    locators = {'': (MobileBy.ID, ''),
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
