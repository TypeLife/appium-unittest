from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetSeeQRCodePage(BasePage):
    """群二维码页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupQRActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '群二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/group_qr_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_layout'),
                  'com.chinasofti.rcs:id/group_info': (MobileBy.ID, 'com.chinasofti.rcs:id/group_info'),
                  '群聊0010': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_name'),
                  'com.chinasofti.rcs:id/photo': (MobileBy.ID, 'com.chinasofti.rcs:id/photo'),
                  'com.chinasofti.rcs:id/left_up': (MobileBy.ID, 'com.chinasofti.rcs:id/left_up'),
                  'com.chinasofti.rcs:id/group_qr_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_icon'),
                  'com.chinasofti.rcs:id/right_up': (MobileBy.ID, 'com.chinasofti.rcs:id/right_up'),
                  'com.chinasofti.rcs:id/left_below': (MobileBy.ID, 'com.chinasofti.rcs:id/left_below'),
                  'com.chinasofti.rcs:id/right_below': (MobileBy.ID, 'com.chinasofti.rcs:id/right_below'),
                  '该二维码7天内(11月22日前)有效': (MobileBy.ID, 'com.chinasofti.rcs:id / group_qr_date'),
                  'com.chinasofti.rcs:id/qecode_share_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_share_btn'),
                  'com.chinasofti.rcs:id/qecode_save_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_save_btn')
                  }
