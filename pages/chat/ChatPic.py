from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatPicPage(BasePage):
    """选择照片页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GalleryActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
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
                  '视频时长': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_time'),
                  'com.chinasofti.rcs:id/rl_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_panel'),
                  '所有视频': (MobileBy.XPATH, "//*[@resource-id='com.chinasofti.rcs:id/iv_video_icon']/../android.widget.RelativeLayout[@resource-id='com.chinasofti.rcs:id/rliv_select']"),
                  '所有图片': (MobileBy.XPATH, "//android.widget.RelativeLayout[@resource-id='com.chinasofti.rcs:id/rl_img']/android.widget.RelativeLayout[1][not(contains(@resource-id,'com.chinasofti.rcs:id/iv_video_icon'))]"),
                  '预览': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_preview'),
                  '原图': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_original_photo'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/button_send')
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待选择照片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["所有照片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def select_video(self, n=0):
        """选择视频
         :Args: - n  - 第n个视频
        """
        videos = self.get_elements(self.__class__.__locators["所有视频"])
        if videos:
            try:
                videos[n].click()
            except:
                raise AssertionError("There is no %s video." % (n+1))
        else:
            raise AssertionError("no video")

    @TestLogger.log()
    def get_video_times(self):
        """获取视频时长"""
        videos = self.get_elements(self.__class__.__locators["视频时长"])
        times = []
        if videos:
            for el in videos:
                times.append(el.text)
            return times
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
    def click_pic_preview(self):
        """点击图片阅览"""
        pics = self.get_elements(self.__class__.__locators["所有图片"])
        if not pics:
            raise AssertionError("There is no pic.")
        pics[0].click()
        pics[0].parent.find_element(MobileBy.ID, 'com.chinasofti.rcs:id/iv_gallery').click()

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(times)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

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

    @TestLogger.log()
    def get_pic_send_num(self):
        """获取图片发送数量"""
        el = self.get_element(self.__class__.__locators["发送"])
        info = el.text
        num = info[-2]
        return num
