from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class NameCardPage(BasePage):
    """个人名片"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UserProfileShowActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        'com.chinasofti.rcs:id/proflie_edit': (MobileBy.ID, 'com.chinasofti.rcs:id/proflie_edit'),
        '编辑': ('xpath',
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.TextView'),
        'com.chinasofti.rcs:id/profile_photo_out': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo_out'),
        'com.chinasofti.rcs:id/profile_name': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_name'),
        'com.chinasofti.rcs:id/profile_photo': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo'),
        '电话': ('xpath',
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[1]'),
        '19876283465': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone_number'),
        '公司': ('xpath',
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[3]'),
        '公司名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_school'),
        '职位': ('xpath',
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[5]'),
        '职位名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profession'),
        '邮箱': ('xpath',
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[7]'),
        '邮箱地址': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_email'),
        '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card')
    }

    @TestLogger.log('分享名片')
    def click_share_btn(self):
        self.swipe_by_percent_on_screen(50, 60, 50, 40, 800)
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log('点击编辑')
    def click_edit(self):
        self.click_element(self.__locators['编辑'])

    @TestLogger.log('获取名片信息')
    def get_name_card_info(self):
        info = dict()
        info['name'] = self.get_text(self.__locators['com.chinasofti.rcs:id/profile_name'])
        info['tel'] = self.get_text(self.__locators['19876283465'])
        info['company'] = self.get_text(self.__locators['公司名字'])
        info['position'] = self.get_text(self.__locators['职位名字'])
        info['email'] = self.get_text(self.__locators['邮箱地址'])
        return info