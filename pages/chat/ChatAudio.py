from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatAudioPage(BasePage):
    """聊天语音页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  'com.chinasofti.rcs:id/back_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '群聊0012(3)': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/iv_slient': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_slient'),
                  'com.chinasofti.rcs:id/action_multicall': (MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                  'com.chinasofti.rcs:id/action_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  'com.chinasofti.rcs:id/imgae_fl': (MobileBy.ID, 'com.chinasofti.rcs:id/imgae_fl'),
                  'com.chinasofti.rcs:id/layout_loading': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  'com.chinasofti.rcs:id/imageview_msg_image': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '17:48': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'mobile952': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  '1': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_send': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
                  'com.chinasofti.rcs:id/ll_more': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_more'),
                  'com.chinasofti.rcs:id/fl_more': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_more'),
                  'com.chinasofti.rcs:id/message_audito_text_root_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/message_audito_text_root_view'),
                  'com.chinasofti.rcs:id/message_audio_record_root_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/message_audio_record_root_view'),
                  '无法识别，请重试': (MobileBy.ID, 'com.chinasofti.rcs:id/recoder_tip'),
                  'com.chinasofti.rcs:id/record_audio_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/record_audio_btn'),
                  '退出': (MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_exit'),
                  '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'),
                  # 语音发送模式选择页面
                  '请选择您偏好的语音发送模式:': (MobileBy.XPATH, '//*[@text="请选择您偏好的语音发送模式:")]'),
                  '同时发送语音+文字(语音识别)': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_and_text'),
                  '仅发送文字(语音识别)': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_text'),
                  '仅发送语音': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'),
                  '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_cancel'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'),
                  '选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/select_send_audio_type_root_view"]/android.widget.LinearLayout/android.widget.ImageView[@selected="true"]/../android.widget.TextView'),
                  '未选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/select_send_audio_type_root_view"]/android.widget.LinearLayout/android.widget.ImageView[@selected="false"]/../android.widget.TextView'),
                  # 弹窗权限页面
                  '不再询问': (MobileBy.ID, 'com.lbe.security.miui:id/do_not_ask_checkbox'),
                  '要允许 和飞信 录制音频吗？': (MobileBy.ID, 'com.android.packageinstaller:id/permission_message'),
                  '拒绝': (MobileBy.ID, 'android:id/button2'),
                  '允许': (MobileBy.XPATH, "//*[contains(@text, '始终允许')]"),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'),
                  '语音+文字选项': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_and_text_icon'),
                  '我知道了': (MobileBy.XPATH, "//*[contains(@text, '我知道了')]"),
                  '仅发送语音选择': (MobileBy.ID, "com.chinasofti.rcs:id/select_send_audio_root"),
                  }

    @TestLogger.log()
    def click_exit(self):
        """点击退出"""
        self.click_element(self.__class__.__locators["退出"])

    @TestLogger.log()
    def get_selected_item(self):
        """获取选择的语音模式"""
        return self.get_element(self.__class__.__locators["选项"]).text

    @TestLogger.log()
    def select_other_audio_item(self):
        """选择其它语音模式项"""
        self.click_element(self.__class__.__locators["未选项"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待聊天语音页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["退出"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_audio_type_select_page_load(self, timeout=2, auto_accept_alerts=False):
        """等待语音发送模式选择页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['仅发送语音'])
            )
            return True
        except:
            return False


    @TestLogger.log()
    def wait_for_audio_allow_page_load(self, timeout=4, auto_accept_alerts=False):
        """等待语音权限申请允许弹窗页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['要允许 和飞信 录制音频吗？'])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_allow(self):
        """点击允许"""
        self.click_element(self.__class__.__locators["允许"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_only_voice(self):
        """点击仅发送语音"""
        self.click_element(self.__class__.__locators["仅发送语音"])

    @TestLogger.log()
    def click_only_text_voice(self):
        """点击 仅发送文字(语音识别)"""
        self.click_element(self.__class__.__locators["仅发送文字(语音识别)"])

    @TestLogger.log()
    def click_only_voice_631(self):
        """点击仅发送语音"""
        self.click_element(self.__class__.__locators["仅发送语音选择"])

    @TestLogger.log()
    def click_send_bottom(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_setting_bottom(self):
        """点击设置"""
        self.click_element(self.__class__.__locators["设置"])

    @TestLogger.log()
    def is_exist_setting_bottom(self, timeout=4, auto_accept_alerts=True):
        """设置是否存在"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("设置")
            )
            return True
        except:
            return False

    @TestLogger.log()
    def get_audio_and_text_icon_selected(self):
        """获取语音+文字模式的选项selected状态"""
        return self.get_element(self.__class__.__locators["语音+文字选项"]).get_attribute("selected")

    @TestLogger.log()
    def click_i_know(self):
        """点击我知道了"""
        self.click_element(self.__class__.__locators["我知道了"])
