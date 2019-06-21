import time

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
                  '返回': (MobileBy.XPATH, "//*[contains(@resource-id, 'back')]"),
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
                  '无搜索结果': (MobileBy.ID, 'com.chinasofti.rcs:id/empty_view'),
                  '发送人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '发送人名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
                  '发送内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
                  '发送时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
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
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators["输入关键词快速搜索"])

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

    @TestLogger.log()
    def select_message_record_by_text(self, text):
        """根据文本消息选择一条消息记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_content" and @text="%s"]' % text)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def is_exists_sending_head(self):
        """是否存在发送人头像"""
        return self._is_element_present(self.__class__.__locators["发送人头像"])

    @TestLogger.log()
    def is_exists_sending_name(self):
        """是否存在发送人名称"""
        return self._is_element_present(self.__class__.__locators["发送人名称"])

    @TestLogger.log()
    def is_exists_send_content(self):
        """是否存在发送内容"""
        return self._is_element_present(self.__class__.__locators["发送内容"])

    @TestLogger.log()
    def is_exists_send_time(self):
        """是否存在发送时间"""
        return self._is_element_present(self.__class__.__locators["发送时间"])
    def check_search_result(self):
        """校验搜索结果"""
        self.page_should_contain_element(self.__class__.__locators["发送人头像"])
        self.page_should_contain_element(self.__class__.__locators["发送人名称"])
        self.page_should_contain_element(self.__class__.__locators["发送内容"])
        self.page_should_contain_element(self.__class__.__locators["发送时间"])

    def check_no_search_result(self, timeout=8, auto_accept_alerts=True):
        """校验无搜索结果"""
        time.sleep(2)
        self.page_should_contain_text('无搜索结果')

    @TestLogger.log()
    def click_search_result(self,result):
        """点击搜索结果"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_content" and @text ="%s"]' % result))

