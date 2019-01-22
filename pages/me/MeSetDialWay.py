from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetDialWayPage(BasePage):
    """我-》设置-》拨号设置-》拨号方式"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.CallTypeSettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '拨号方式': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                '总是询问': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_alaways_ask'),
                'com.chinasofti.rcs:id/call_type_alaways_ask': (
                MobileBy.ID, 'com.chinasofti.rcs:id/call_type_alaways_ask'),
                'com.chinasofti.rcs:id/rl_fetion': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_fetion'),
                '优先使用和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_call_type_prior_fetioncall'),
                'com.chinasofti.rcs:id/iv_call_type_prior_fetioncall': (
                MobileBy.ID, 'com.chinasofti.rcs:id/iv_call_type_prior_fetioncall'),
                'com.chinasofti.rcs:id/line_fetion': (MobileBy.ID, 'com.chinasofti.rcs:id/line_fetion'),
                '只用语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_only_yuying'),
                'com.chinasofti.rcs:id/call_type_only_yuying': (
                MobileBy.ID, 'com.chinasofti.rcs:id/call_type_only_yuying'),
                '只用普通电话': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_only_normal'),
                'com.chinasofti.rcs:id/call_type_only_normal': (
                MobileBy.ID, 'com.chinasofti.rcs:id/call_type_only_normal'),
                '自动推荐': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_auto_give'),
                'com.chinasofti.rcs:id/call_type_auto_give': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_auto_give'),
                'com.chinasofti.rcs:id/call_type_tips': (MobileBy.ID, 'com.chinasofti.rcs:id/call_type_tips'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
