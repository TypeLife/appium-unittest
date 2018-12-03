from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupSMSExpensesRemindPage(BasePage):
    """资费提醒页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSMSEditActivity'

    __locators = {'': (MobileBy.ID, ''),
 'android:id/content': (MobileBy.ID, 'android:id/content'),
 '资费提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_title'),
 '中国移动用户使用群短信功能给中国移动用户群成员发送短信，免收短信费；给非中国移动用户群成员发送短信将收取0.01元/条。': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
 'com.chinasofti.rcs:id/btn_container': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_container'),
 '我知道了': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok')
}
