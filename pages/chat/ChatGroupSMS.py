from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupSMSPage(BasePage):
    """群短信编辑页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSMSEditActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '群短信': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/context_fragment': (MobileBy.ID, 'com.chinasofti.rcs:id/context_fragment'),
                  '接收人：': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_sendee'),
                  'com.chinasofti.rcs:id/select_sendee': (MobileBy.ID, 'com.chinasofti.rcs:id/select_sendee'),
                  'com.chinasofti.rcs:id/layout_for_sms': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_sms'),
                  'com.chinasofti.rcs:id/sms_direction': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'),
                  '您正在使用群短信功能': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_isFree'),
                  'com.chinasofti.rcs:id/layout_sms_pannel': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_sms_pannel'),
                  '发送短信...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_edit'),
                  'com.chinasofti.rcs:id/tv_send': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send')
                  }
