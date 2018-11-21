from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatPhotoPage(BasePage):
    """聊天拍照页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.VideoRecordActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/fl_content': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_content'),
                  'com.chinasofti.rcs:id/recordSurfaceView': (MobileBy.ID, 'com.chinasofti.rcs:id/recordSurfaceView'),
                  'com.chinasofti.rcs:id/bottomLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/bottomLayout'),
                  'com.chinasofti.rcs:id/record_parent': (MobileBy.ID, 'com.chinasofti.rcs:id/record_parent'),
                  '轻触拍照,长按录像': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_duration_recording_tv'),
                  'com.chinasofti.rcs:id/rl_back': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_back'),
                  '取消拍照': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_back'),
                  '拍照': (MobileBy.ID, 'com.chinasofti.rcs:id/record'),
                  '切换前后摄像头': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_change_camera_bt'),
                  # 拍照后的页面控件
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/send'),
                  '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/img_edit'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/rerecord'),
                  }

    @TestLogger.log()
    def take_photo(self):
        """拍照"""
        self.click_element(self.__class__.__locators["拍照"])

    @TestLogger.log()
    def take_photo_back(self):
        """拍照返回"""
        self.click_element(self.__class__.__locators["取消拍照"])

    @TestLogger.log()
    def send_photo(self):
        """发送照片"""
        self.click_element(self.__class__.__locators["发送"])
