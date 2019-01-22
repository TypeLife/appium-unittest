from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage


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
        self.click_element(self.__class__.__locators["选择名片"])

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
