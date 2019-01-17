from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatPicEditPage(BasePage):
    """选择照片->预览->编辑 页面"""
    ACTIVITY = 'com.juphoon.imgeditor.PictureEditActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/vs_op': (MobileBy.ID, 'com.chinasofti.rcs:id/vs_op'),
                  '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_cancel'),
                  '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_done'),
                  'com.chinasofti.rcs:id/rg_modes': (MobileBy.ID, 'com.chinasofti.rcs:id/rg_modes'),
                  '涂鸦': (MobileBy.ID, 'com.chinasofti.rcs:id/rb_doodle'),
                  '马赛克': (MobileBy.ID, 'com.chinasofti.rcs:id/rb_mosaic'),
                  '文本编辑按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_text'),
                  'com.chinasofti.rcs:id/btn_clip': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_clip'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send'),
                  'com.chinasofti.rcs:id/image_canvas': (MobileBy.ID, 'com.chinasofti.rcs:id/image_canvas'),
                  # 文本编辑页面
                  '文本编辑框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_text'),
                  }

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_cancle(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def click_doodle(self):
        """点击涂鸦"""
        self.click_element(self.__class__.__locators["涂鸦"])

    @TestLogger.log()
    def do_doodle(self):
        """涂鸦操作"""
        self.swipe_by_percent_on_screen(40, 45, 60, 45, 800)
        self.swipe_by_percent_on_screen(30, 55, 70, 55, 800)

    @TestLogger.log()
    def click_mosaic(self):
        """点击马赛克"""
        self.click_element(self.__class__.__locators["马赛克"])

    @TestLogger.log()
    def do_mosaic(self):
        """马赛克操作"""
        self.swipe_by_percent_on_screen(40, 45, 60, 45, 800)
        self.swipe_by_percent_on_screen(30, 55, 70, 55, 800)

    @TestLogger.log()
    def click_text_edit_btn(self):
        """点击文本编辑按钮"""
        self.click_element(self.__class__.__locators["文本编辑按钮"])

    @TestLogger.log()
    def input_pic_text(self, text="PicTextEdit"):
        """输入编辑文本"""
        self.input_text(self.__class__.__locators["文本编辑框"], text)

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(times)
