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
                  '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish')
                  }

    @TestLogger.log()
    def click_exit(self):
        """点击退出"""
        self.click_element(self.__class__.__locators["退出"])

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
