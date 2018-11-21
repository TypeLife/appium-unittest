from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatPicPage(BasePage):
    """群聊选择照片页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GalleryActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '所有照片': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/select_rl': (MobileBy.ID, 'com.chinasofti.rcs:id/select_rl'),
                  'com.chinasofti.rcs:id/drop_down_image': (MobileBy.ID, 'com.chinasofti.rcs:id/drop_down_image'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/recyclerView_gallery': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_gallery'),
                  'com.chinasofti.rcs:id/rl_img': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_img'),
                  'com.chinasofti.rcs:id/iv_video_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_video_icon'),
                  'com.chinasofti.rcs:id/imageview_video_start_background': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/imageview_video_start_background'),
                  'com.chinasofti.rcs:id/imageview_video_start': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/imageview_video_start'),
                  '00:02': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_time'),
                  'com.chinasofti.rcs:id/iv_gallery': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_gallery'),
                  'com.chinasofti.rcs:id/rliv_select': (MobileBy.ID, 'com.chinasofti.rcs:id/rliv_select'),
                  'com.chinasofti.rcs:id/iv_select': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_select'),
                  '00:03': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_time'),
                  'com.chinasofti.rcs:id/rl_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_panel'),
                  '所有视频': (MobileBy.XPATH, "//*[@resource-id='com.chinasofti.rcs:id/iv_video_icon']/../android.widget.RelativeLayout[@resource-id='com.chinasofti.rcs:id/rliv_select']"),
                  '所有图片': (MobileBy.XPATH, "//android.widget.RelativeLayout[@resource-id='com.chinasofti.rcs:id/rl_img']/android.widget.RelativeLayout[1][not(contains(@resource-id,'com.chinasofti.rcs:id/iv_video_icon'))]"),
                  '预览': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_preview'),
                  '原图': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_original_photo'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/button_send')
                  }

    @TestLogger.log()
    def select_video(self, n=0):
        """选择视频
         :Args:
         - n   - 第n个视频
        """
        videos = self.get_elements(self.__class__.__locators["所有视频"])
        if videos:
            try:
                videos[n].click()
            except:
                raise AssertionError("There is no %s video." % n)
        else:
            raise AssertionError("no video")

    @TestLogger.log()
    def select_pic(self, n=1):
        """选择n个图片"""
        pics = self.get_elements(self.__class__.__locators["所有图片"])
        if n > len(pics):
            raise AssertionError("There is no %s pic." % n)
        for i in range(n):
            pics[i].click()

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_preview(self):
        """点击预览"""
        self.click_element(self.__class__.__locators["预览"])

    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])

    @TestLogger.log()
    def send_preview_is_enabled(self):
        """获取预览按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["预览"])
