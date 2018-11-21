from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatSelectFilePage(BasePage):
    """聊天选择文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChooseLocalFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '选择文件': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/fl_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_container'),
                  '本地文件': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'),
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_vedio'),
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_pic'),
                  '音乐': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_music'),
                  }

    @TestLogger.log()
    def click_local_file(self):
        """点击本地文件"""
        self.click_element(self.__class__.__locators["本地文件"])

    @TestLogger.log()
    def click_video(self):
        """点击视频"""
        self.click_element(self.__class__.__locators["视频"])

    @TestLogger.log()
    def click_pic(self):
        """点击照片"""
        self.click_element(self.__class__.__locators["照片"])

    @TestLogger.log()
    def click_music(self):
        """点击音乐"""
        self.click_element(self.__class__.__locators["音乐"])
