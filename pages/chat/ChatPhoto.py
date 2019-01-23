from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from appium.webdriver.common.touch_action import TouchAction

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
                  # 发送录像后的弹出页面
                  '继续发送': (MobileBy.ID, 'com.chinasofti.rcs:id/continue_call'),
                  '订购免流特权': (MobileBy.ID, 'com.chinasofti.rcs:id/get_mian_liu_permission'),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待聊天拍照页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["轻触拍照,长按录像"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_record_video_after_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待聊天拍照之后的页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["返回"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def take_photo(self):
        """拍照"""
        self.click_element(self.__class__.__locators["拍照"])
        time.sleep(3)

    @TestLogger.log()
    def take_photo_back(self):
        """拍照返回"""
        self.click_element(self.__class__.__locators["取消拍照"])

    @TestLogger.log()
    def click_edit_pic(self):
        """点击编辑拍摄的照片"""
        self.click_element(self.__class__.__locators["编辑"])

    @TestLogger.log()
    def send_photo(self, times=5):
        """发送照片"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(times)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def record_video(self, times):
        """录像"""
        el = self.get_element(self.__class__.__locators["拍照"])
        self.press(el, times=times)

    @TestLogger.log()
    def send_video(self, times=5):
        """发送录像"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(1)
        # 弹出窗处理
        if self.is_text_present("继续发送"):
            self.click_element(self.__class__.__locators["继续发送"])
        time.sleep(times)

