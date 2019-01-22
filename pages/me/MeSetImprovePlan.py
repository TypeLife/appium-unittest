from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetImprovePlanPage(BasePage):
    """我-》设置-》参与体验改善计划"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UploadLogActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '参与体验改善计划': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                '使用和飞信中如发生功能异常等问题': (MobileBy.ID, ''),
                '请上传日志帮助我们更好定位和解决问题。': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/btn_send': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send'),
                '上传日志': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send'),
                '日志中仅包含最近时间段内和飞信的故障记录、技术数据及其他必要的系统信息，不包括聊天记录等信息': (MobileBy.ID, ''),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
