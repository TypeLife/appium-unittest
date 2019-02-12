from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MutiVideoPage(BasePage):
    """
    通讯录 - 标签分组 - 多方视频主叫页面
    """
    ACTIVITY = 'com.cmicc.module_call.ui.activity.MultiVideoActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/ll_multi_video_talking': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_multi_video_talking'),
        'com.chinasofti.rcs:id/call_setting_operation_layout': (
            MobileBy.ID, 'com.chinasofti.rcs:id/call_setting_operation_layout'),
        'com.chinasofti.rcs:id/iv_hide': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_hide'),
        'com.chinasofti.rcs:id/multi_video_add_person': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_video_add_person'),
        'com.chinasofti.rcs:id/rv_show_video': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_show_video'),
        'com.chinasofti.rcs:id/card': (MobileBy.ID, 'com.chinasofti.rcs:id/card'),
        'com.chinasofti.rcs:id/iv_item_small_switch_camera': (
            MobileBy.ID, 'com.chinasofti.rcs:id/iv_item_small_switch_camera'),
        '00:06': (MobileBy.ID, 'com.chinasofti.rcs:id/call_duration_text'),
        'com.chinasofti.rcs:id/rl_operation': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_operation'),
        'com.chinasofti.rcs:id/iv_open_self_camera': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_open_self_camera'),
        'com.chinasofti.rcs:id/mutil_video_call_speaker_btn': (
            MobileBy.ID, 'com.chinasofti.rcs:id/mutil_video_call_speaker_btn'),
        'com.chinasofti.rcs:id/mutil_video_call_mute': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_video_call_mute'),
        'com.chinasofti.rcs:id/end_video_call_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/end_video_call_btn'),
        'com.chinasofti.rcs:id/ll_tv_hint': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_tv_hint'),
        '关闭摄像头': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_open'),
        '免提': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_multi_speaker'),
        '静音': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_multi_mute')
    }
