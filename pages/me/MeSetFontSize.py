from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MeSetFontSizePage(BasePage):
    """我-》设置-》设置字体大小"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.FontSettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/title_bar': (MobileBy.ID, 'com.chinasofti.rcs:id/title_bar'),
                'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                '设置字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                '确认': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send'),
                'com.chinasofti.rcs:id/text_font_group1': (MobileBy.ID, 'com.chinasofti.rcs:id/text_font_group1'),
                '预览字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_size_text'),
                'com.chinasofti.rcs:id/font_setting_avatar_view': (
                MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_avatar_view'),
                'com.chinasofti.rcs:id/text_font_group2': (MobileBy.ID, 'com.chinasofti.rcs:id/text_font_group2'),
                '拖动下面的滑动，可设置字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_size_text_2'),
                'com.chinasofti.rcs:id/font_setting_avatar_view_2': (
                MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_avatar_view_2'),
                'com.chinasofti.rcs:id/text_font_group3': (MobileBy.ID, 'com.chinasofti.rcs:id/text_font_group3'),
                '设置好，会改变聊天，菜单的字体大小。如果在使用过程中存在问题和意见，可反馈给我们团队': (MobileBy.ID, 'com.chinasofti.rcs:id/font_size_text_3'),
                'com.chinasofti.rcs:id/font_setting_avatar_view_3': (
                MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_avatar_view_3'),
                'com.chinasofti.rcs:id/font_size_setting_view': (
                MobileBy.ID, 'com.chinasofti.rcs:id/font_size_setting_view'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }
