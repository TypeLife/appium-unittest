from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetPicVideoPage(BasePage):
    """查找聊天内容中编辑图片"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChatFileActivity'

    __locators = {
                  '返回': (MobileBy.XPATH, "//*[contains(@resource-id, 'back')]"),
                  '图片与视频标题': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '图片与视频': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_thumb'),
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/video_duration'),
                  'com.chinasofti.rcs:id/result_list': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '保存图片': (MobileBy.XPATH, "//*[contains(@text, '保存图片')]"),
                  '保存视频': (MobileBy.XPATH, "//*[contains(@text, '保存视频')]"),
                  '编辑': (MobileBy.XPATH, "//*[contains(@text, '编辑')]"),
                  '预览该图片视频': (MobileBy.ID, "com.chinasofti.rcs:id/vp_preview"),
                  '预览该视频': (MobileBy.ID, "com.chinasofti.rcs:id/surface"),
                  '关闭预览视频': (MobileBy.ID, "com.chinasofti.rcs:id/iv_close"),
                  "识别图中二维码": (MobileBy.XPATH, '//*[@text="识别图中二维码"]'),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待查找聊天内容页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["图片与视频标题"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def press_file_to_do(self, text):
        """长按图片与视频进行操作"""
        el = self.get_element(self.__class__.__locators['图片与视频'])
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_pic_video(self):
        """点击该图片和视频"""
        self.click_element(self.__class__.__locators['图片与视频'])

    @TestLogger.log()
    def click_video(self):
        """点击该视频"""
        self.click_element(self.__class__.__locators['视频'])

    @TestLogger.log()
    def click_pre_pic_video(self):
        """点击该预览图片和视频"""
        self.click_element(self.__class__.__locators['预览该图片视频'])

    @TestLogger.log()
    def press_pre_video_to_do(self, text):
        """长按预览视频进行操作"""
        el = self.get_element(self.__class__.__locators['预览该视频'])
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_pre_file_to_do(self, text):
        """长按预览图片与视频进行操作"""
        el = self.get_element(self.__class__.__locators['预览该图片视频'])
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_toast_exist_zf(self):
        """是否存在已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def is_toast_exist_sc(self):
        """是否存在已收藏"""
        return self.is_toast_exist("已收藏")

    @TestLogger.log()
    def is_toast_exist_save(self):
        """是否存在保存成功"""
        return self.is_toast_exist("保存成功")

    @TestLogger.log()
    def is_toast_exist_save_video(self):
        """是否存在保存成功"""
        return self.is_toast_exist("视频已保存")

    @TestLogger.log()
    def click_close_pre_video(self):
        """点击关闭该预览视频"""
        self.click_element(self.__class__.__locators['关闭预览视频'])
