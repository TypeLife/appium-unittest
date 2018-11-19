from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatPage(BasePage):
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
                  '群聊001(2)': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/action_multicall': (MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                  'com.chinasofti.rcs:id/action_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
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
                  'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
                  'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
                  '选择图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '选择相机': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  '选择gif': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_gif'),
                  '选择更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  'com.chinasofti.rcs:id/ib_audio': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  'com.chinasofti.rcs:id/ib_record_red_dot': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_record_red_dot')
                  }

    @TestLogger.log()
    def click_pic(self):
        """点击选择图片"""
        self.click_element(self.__class__.__locators["选择图片"])

    @TestLogger.log()
    def click_take_photo(self):
        """点击选择相机"""
        self.click_element(self.__class__.__locators["选择相机"])

    @TestLogger.log()
    def click_profile(self):
        """点击选择联系人"""
        self.click_element(self.__class__.__locators["选择联系人"])

    @TestLogger.log()
    def click_gif(self):
        """点击选择gif"""
        self.click_element(self.__class__.__locators["选择gif"])

    @TestLogger.log()
    def click_more(self):
        """点击选择更多"""
        self.click_element(self.__class__.__locators["选择更多"])

