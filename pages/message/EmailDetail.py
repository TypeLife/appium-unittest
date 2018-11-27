from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class EmailDetailPage(BasePage):
    """邮件详情"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.WebViewActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/RelativeLayout1': (MobileBy.ID, 'com.chinasofti.rcs:id/RelativeLayout1'),
                  'com.chinasofti.rcs:id/title_main_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/title_main_layout'),
                  'com.chinasofti.rcs:id/ll_back': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_back'),
                  'com.chinasofti.rcs:id/btn_back': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
                  '邮件全文': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_title'),
                  'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
                  }
