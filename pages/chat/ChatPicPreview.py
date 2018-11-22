from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatPicPreviewPage(BasePage):
    """群聊选择照片->预览 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GalleryChangedActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '预览(1/2)': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_editimage'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/vp_preview': (MobileBy.ID, 'com.chinasofti.rcs:id/vp_preview'),
                  'com.chinasofti.rcs:id/pv_item': (MobileBy.ID, 'com.chinasofti.rcs:id/pv_item'),
                  'com.chinasofti.rcs:id/iv_smooth': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_smooth'),
                  'com.chinasofti.rcs:id/rl_select_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_select_panel'),
                  'com.chinasofti.rcs:id/ll_select': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_select'),
                  'com.chinasofti.rcs:id/iv_select': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_select'),
                  '选择': (MobileBy.ID, ''),
                  '原图': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_original_photo'),
                  '发送(2)': (MobileBy.ID, 'com.chinasofti.rcs: id /btn_send ')
                  }

    @TestLogger.log()
    def get_pic_preview_num(self):
        """获取预览数"""
        el = self.get_element(self.__class__.__locators["预览(1/2)"])
        info = el.text
        num = info[-2]
        return num

    @TestLogger.log()
    def get_pic_preview_info(self):
        """获取预览信息"""
        el = self.get_element(self.__class__.__locators["预览(1/2)"])
        return el.text

    @TestLogger.log()
    def get_pic_send_num(self):
        """获取图片发送数量"""
        el = self.get_element(self.__class__.__locators["发送(2)"])
        info = el.text
        num = info[-2]
        return num
