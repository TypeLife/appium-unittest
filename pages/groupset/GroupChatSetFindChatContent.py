from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetFindChatContentPage(BasePage):
    """查找聊天内容"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageSearchActivity'

    __locators = {
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_back'),
                  'com.chinasofti.rcs:id/iv_back': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  '输入关键词快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
                  '分类索引': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint_2'),
                  'com.chinasofti.rcs:id/layout_file_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_file_search'),
                  '文件': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_search'),
                  'com.chinasofti.rcs:id/layout_video_img_search': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_video_img_search'),
                  '图片与视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_img_search'),
                  'com.chinasofti.rcs:id/result_list': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
                  # 搜索无结果页
                  'X': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
                  '无搜索结果': (MobileBy.ID, 'com.chinasofti.rcs:id/empty_view')
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待查找聊天内容页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["分类索引"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def search(self, chat_context):
        """搜索聊天内容"""
        self.input_text(self.__class__.__locators["输入关键词快速搜索"], chat_context)

    @TestLogger.log()
    def click_x_icon(self):
        """点击X"""
        self.click_element(self.__class__.__locators["X"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_pic_video(self):
        """点击图片与视频"""
        self.click_element(self.__class__.__locators["图片与视频"])

