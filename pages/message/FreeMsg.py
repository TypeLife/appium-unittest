from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class FreeMsgPage(BasePage):
    """免费短信"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.SuperMsgActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/super_msg_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/super_msg_layout'),
        '欢迎使用免费短信！': (MobileBy.ID, 'com.chinasofti.rcs:id/free_message'),
        'com.chinasofti.rcs:id/image_bg': (MobileBy.ID, 'com.chinasofti.rcs:id/image_bg'),
        'com.chinasofti.rcs:id/ll': (MobileBy.ID, 'com.chinasofti.rcs:id/ll'),
        '启用和飞信收发免费短信': (MobileBy.ID, 'com.chinasofti.rcs:id/group_tip'),
        '你可': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip2'),
        '免费给移动用户发送短信，': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip3'),
        '给非移动用户发短信将收取0.01元/条，': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip'),
        '给港澳台等境外用户发短信将收取1元/条。': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip_more'),
        'com.chinasofti.rcs:id/ll_bt': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_bt'),
        '以后再说': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_btn'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn')
    }

    @TestLogger.log()
    def click_cancle_btn(self):
        """点击以后再说"""
        self.click_element(self.__locators['以后再说'])

    @TestLogger.log()
    def click_sure_btn(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def is_exist_cancle_btn(self):
        """判断以后再说是否存在"""
        return self._is_element_present(self.__class__.__locators["以后再说"])
