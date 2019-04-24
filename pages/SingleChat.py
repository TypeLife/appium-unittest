from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage
import time


class SingleChatPage(BaseChatPage):
    """单聊会话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  'axzq': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '打电话图标': (MobileBy.ID, 'com.chinasofti.rcs:id/action_call'),
                  '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  'com.chinasofti.rcs:id/linearLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/linearLayout'),
                  '10:57': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/ll_msg': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_msg'),
                  'com.chinasofti.rcs:id/iv_file_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_file_icon'),
                  '67.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '和飞信测试用例.xlsx': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  'com.chinasofti.rcs:id/img_message_down_file': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '对方离线，已提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_has_read'),
                  'com.chinasofti.rcs:id/iv_send_status': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_send_status'),
                  'com.chinasofti.rcs:id/imgae_fl': (MobileBy.ID, 'com.chinasofti.rcs:id/imgae_fl'),
                  'com.chinasofti.rcs:id/layout_loading': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  'com.chinasofti.rcs:id/imageview_msg_image': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  'hello': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '选择短信': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  '语音消息体': (MobileBy.ID, 'com.chinasofti.rcs:id/img_audio_play_icon'),
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '选择照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '短信发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'),
                  '短信输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'),
                  '短信资费提醒': (MobileBy.XPATH, '//*[@text="资费提醒"]'),
                  "文本输入框": (MobileBy.ID, "com.chinasofti.rcs:id/et_message"),
                  "文本发送按钮": (MobileBy.ID, "com.chinasofti.rcs:id/ib_send"),
                  "消息免打扰图标": (MobileBy.ID, "com.chinasofti.rcs:id/iv_slient"),
                  '重发按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                  '文件名称': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name')
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待单聊会话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["打电话图标"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_sms(self):
        """点击选择短信"""
        self.click_element(self.__class__.__locators["选择短信"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在单聊会话页面"""
        el = self.get_elements(self.__locators['打电话图标'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_setting(self):
        """点击 设置"""
        self.click_element(self.__class__.__locators['设置'])

    @TestLogger.log()
    def is_audio_exist(self):
        """是否存在语音消息"""
        return self._is_element_present(self.__class__.__locators['语音消息体'])

    def is_exist_msg_videos(self):
        """当前页面是否有发视频消息"""
        el = self.get_elements(self.__class__.__locators['消息视频'])
        return len(el) > 0

    def is_exist_msg_image(self):
        """当前页面是否有发图片消息"""
        el = self.get_elements(self.__class__.__locators['消息图片'])
        return len(el) > 0

    @TestLogger.log()
    def click_picture(self):
        """点击选择照片"""
        self.click_element(self.__class__.__locators["选择照片"])

    @TestLogger.log()
    def is_exist_forward(self):
        """是否存在消息已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def is_enabled_sms_send_btn(self):
        """短信发送按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators['短信发送按钮'])

    @TestLogger.log()
    def input_sms_message(self, message):
        """输入短信信息"""
        self.input_text(self.__class__.__locators["短信输入框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def send_sms(self):
        """发送短信"""
        self.click_element(self.__class__.__locators["短信发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_present_sms_fee_remind(self, timeout=3, auto_accept_alerts=True):
        """是否出现短信资费提醒窗"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["短信资费提醒"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def input_text_message(self, message):
        """输入文本信息"""
        self.input_text(self.__class__.__locators["文本输入框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def send_text(self):
        """发送文本"""
        self.click_element(self.__class__.__locators["文本发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_exist_no_disturb_icon(self):
        """是否存在消息免打扰图标"""
        return self._is_element_present(self.__class__.__locators["消息免打扰图标"])

    @TestLogger.log()
    def is_exist_file_by_type(self, file_type):
        """是否存在指定类型文件"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and contains(@text,"%s")]' % file_type)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_exist_msg_send_failed_button(self):
        """是否存在重发按钮"""
        return self._is_element_present(self.__class__.__locators["重发按钮"])

    @TestLogger.log()
    def click_msg_send_failed_button(self, number):
        """点击重发按钮"""
        if self._is_element_present(self.__class__.__locators['重发按钮']):
            els = self.get_elements(self.__class__.__locators["重发按钮"])
            els[number].click()

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def get_current_file_name(self):
        """获取刚刚发送的文件名称"""
        els = self.get_elements(self.__class__.__locators["文件名称"])
        file_name = els[-1].text
        return file_name

    @TestLogger.log()
    def click_action_call(self):
        """点击打电话图标"""
        self.click_element(self.__class__.__locators["打电话图标"])
