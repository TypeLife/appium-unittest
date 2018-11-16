from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetManagerPage(BasePage):
    """群管理页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupManageActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '群管理': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/group_transfer': (MobileBy.ID, 'com.chinasofti.rcs:id/group_transfer'),
                  '群主管理权转让': (MobileBy.ID, 'com.chinasofti.rcs:id/group_transfer_tv'),
                  'com.chinasofti.rcs:id/group_disband': (MobileBy.ID, 'com.chinasofti.rcs:id/group_disband'),
                  '解散群': (MobileBy.ID, 'com.chinasofti.rcs:id/group_disband_tv')
                  }
