from appium.webdriver.common.mobileby import MobileBy

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
                  'com.chinasofti.rcs:id/rb_doodle': (MobileBy.ID, 'com.chinasofti.rcs:id/rb_doodle'),
                  'com.chinasofti.rcs:id/rb_mosaic': (MobileBy.ID, 'com.chinasofti.rcs:id/rb_mosaic'),
                  'com.chinasofti.rcs:id/btn_text': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_text'),
                  'com.chinasofti.rcs:id/btn_clip': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_clip'),
                  'com.chinasofti.rcs:id/btn_send': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send'),
                  'com.chinasofti.rcs:id/image_canvas': (MobileBy.ID, 'com.chinasofti.rcs:id/image_canvas')
                  }
