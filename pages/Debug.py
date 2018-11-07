from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class DebugPage(BasePage):
    """Debug"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {'': (MobileBy.ID, ''),
 'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
 'android:id/content': (MobileBy.ID, 'android:id/content'),
 'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
 'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
 'com.chinasofti.rcs:id/constraintLayout_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
 'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
 'com.chinasofti.rcs:id/titleBar': (MobileBy.ID, 'com.chinasofti.rcs:id/titleBar'),
 '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
 'com.chinasofti.rcs:id/qr_code_imageview': (MobileBy.ID, 'com.chinasofti.rcs:id/qr_code_imageview'),
 'com.chinasofti.rcs:id/layout_for_mall': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_mall'),
 'com.chinasofti.rcs:id/internet_mutil_call_layout_id': (MobileBy.ID, 'com.chinasofti.rcs:id/internet_mutil_call_layout_id'),
 '300': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_number_text'),
 '分钟': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_unit'),
 'com.chinasofti.rcs:id/layout_flow': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_flow'),
 '--': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_number_text'),
 'KB': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_unit'),
 'com.chinasofti.rcs:id/redpager': (MobileBy.ID, 'com.chinasofti.rcs:id/redpager'),
 '钱包': (MobileBy.ID, 'com.chinasofti.rcs:id/repager_text'),
 'com.chinasofti.rcs:id/welfare': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare'),
 '福利': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare_text'),
 '推荐好友，赚现金红包': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
 'com.chinasofti.rcs:id/wfSpace': (MobileBy.ID, 'com.chinasofti.rcs:id/wfSpace'),
 'com.chinasofti.rcs:id/welfareArrow': (MobileBy.ID, 'com.chinasofti.rcs:id/welfareArrow'),
 'com.chinasofti.rcs:id/collect': (MobileBy.ID, 'com.chinasofti.rcs:id/collect'),
 '收藏': (MobileBy.ID, 'com.chinasofti.rcs:id/collect_text'),
 'com.chinasofti.rcs:id/about_app': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app'),
 '关于和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app_text'),
 'com.chinasofti.rcs:id/about_right_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/about_right_arrow'),
 'com.chinasofti.rcs:id/share_app': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app'),
 '分享客户端': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app_text'),
 'com.chinasofti.rcs:id/feedback': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback'),
 '帮助与反馈': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback_text'),
 'com.chinasofti.rcs:id/setting': (MobileBy.ID, 'com.chinasofti.rcs:id/setting'),
 '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_app_text'),
 'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
 'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
 '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
 'com.chinasofti.rcs:id/rnMessageBadge': (MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
 '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
 '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
 '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
 'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
}
