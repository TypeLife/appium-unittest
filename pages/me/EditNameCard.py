from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EditNameCardPage(BasePage):
    """编辑个人名片"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UserProfileEditActivity'

    __locators = {'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
 'android:id/content': (MobileBy.ID, 'android:id/content'),
 'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
 'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
 'com.chinasofti.rcs:id/proflie_save': (MobileBy.ID, 'com.chinasofti.rcs:id/proflie_save'),
 '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save'),
 'com.chinasofti.rcs:id/profile_photo': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo'),
 'com.chinasofti.rcs:id/change_photo': (MobileBy.ID, 'com.chinasofti.rcs:id/change_photo'),
 '姓名': ('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView'),
 '输入姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_name'),
 '电话': ('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView[1]'),
 '19876283465': (MobileBy.ID, 'com.chinasofti.rcs:id/phone'),
 '公司': ('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView'),
 '输入公司': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_company'),
 '职位': ('xpath', '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[4]/android.widget.TextView')
}
