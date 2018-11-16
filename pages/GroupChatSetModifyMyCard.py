from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetModifyMyCardPage(BasePage):
    """修改群名片页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupCardActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '修改群名片': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/group_card_save'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
                  'com.chinasofti.rcs:id/iv_delect': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')
                  }
