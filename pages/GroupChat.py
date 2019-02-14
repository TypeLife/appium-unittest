from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage


class GroupChatPage(BaseChatPage):
    """群聊天页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  'com.chinasofti.rcs:id/back_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '群聊001(2)': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '消息免打扰': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_slient'),
                  '多方通话': (MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                  '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  '14:58': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  '[呲牙1]': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '呵呵': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  'APP test': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  '选择名片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  '更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  '文件发送成功标志': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '选择照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '发送失败标识': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '我知道了': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok'),
                  '勾': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '重发消息确定': (MobileBy.ID, '	com.chinasofti.rcs:id/btn_ok'),
                  }

    def is_exist_msg_videos(self):
        """当前页面是否有发视频消息"""
        el = self.get_elements(self.__locators['消息视频'])
        return len(el) > 0

    def is_exist_msg_image(self):
        """当前页面是否有发图片消息"""
        el = self.get_elements(self.__locators['消息图片'])
        return len(el) > 0

    @TestLogger.log()
    def is_exist_collection(self):
        """是否存在消息已收藏"""
        return self.is_toast_exist("已收藏")

    @TestLogger.log()
    def is_exist_forward(self):
        """是否存在消息已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def click_take_picture(self):
        """点击选择富媒体拍照"""
        self.click_element(self.__class__.__locators["富媒体拍照"])

    @TestLogger.log()
    def is_send_sucess(self):
        """当前页面是否有发送失败标识"""
        el = self.get_elements(self.__locators['发送失败标识'])
        if len(el) > 0:
            return False
        return True

    @TestLogger.log()
    def click_picture(self):
        """点击选择照片"""
        self.click_element(self.__class__.__locators["选择照片"])

    @TestLogger.log()
    def click_setting(self):
        """点击设置"""
        self.click_element(self.__class__.__locators["设置"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待群聊页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方通话"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['多方通话'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_profile(self):
        """点击选择名片"""
        self.click_element(self.__class__.__locators["选择名片"])

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_undisturb(self):
        """是否存在消息免打扰标志"""
        return self._is_element_present(self.__class__.__locators["消息免打扰"])

    @TestLogger.log()
    def click_more(self):
        """点击更多富媒体按钮"""
        self.click_element(self.__class__.__locators["更多"], default_timeout=8)

    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_file(self, file):
        """长按指定文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)

    @TestLogger.log()
    def is_address_text_present(self):
        """判断位置信息是否在群聊页面发送"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def press_message_to_do(self, text):
        """长按指定信息进行操作"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def wait_for_message_down_file(self, timeout=20, auto_accept_alerts=True):
        """等待消息发送成功"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["勾"])
            )
        except:
            message = "消息在{}s内，没有发送成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_exist_network(self):
        """是否存网络不可用"""
        return self.is_toast_exist("网络不可用，请检查网络设置")

    @TestLogger.log()
    def click_send_again(self):
        """点击重新发送gif"""
        self.click_element(self.__class__.__locators["发送失败标识"])
        self.click_element(self.__class__.__locators["重发消息确定"])
