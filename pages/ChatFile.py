from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatFilePage(BasePage):
    """查找聊天内容-》文件-》聊天文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChatFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '聊天文件': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/chat_file_list': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_file_list'),
                  '本月': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
                  'com.chinasofti.rcs:id/favorite_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_layout'),
                  'com.chinasofti.rcs:id/tv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_head'),
                  '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  '今天': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/favorite_image_shortcut': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/favorite_image_shortcut'),
                  'com.chinasofti.rcs:id/favorite_file_name_size': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/favorite_file_name_size'),
                  '文件名': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '录制.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '271.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '445475fa1e154603b4fd64ce34fa8c62.amr': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '3.7KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  # 文件长按弹窗
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def delete_file(self, file):
        """长按文件删除"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['删除'])

    @TestLogger.log()
    def collection_file(self, file):
        """收藏文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['收藏'])

    @TestLogger.log()
    def forward_file(self, file):
        """转发文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['转发'])

    @TestLogger.log()
    def is_on_this_page(self):
        """是否在此页面"""
        if self.is_text_present("本月"):
            return True
        else:
            return False

    @TestLogger.log()
    def clear_file_record(self):
        """清除文件记录"""
        while True:
            els = self.get_elements(self.__class__.__locators['文件名'])
            if not els:
                break
            for el in els:
                self.press(el)
                self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def page_should_contain_file(self):
        """页面应该有文件记录"""
        self.page_should_contain_element(self.__class__.__locators['文件名'])
