from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components import ChatNoticeDialog
from pages.components.selectors import PictureSelector


class ChatWindowPage(ChatNoticeDialog, PictureSelector, BasePage):
    """聊天窗口"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
        '13537795364': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        'com.chinasofti.rcs:id/action_call': (MobileBy.ID, 'com.chinasofti.rcs:id/action_call'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
        'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/message_editor_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
        'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
        '星期三 20:50': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
        '11': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
        'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_sms_mark': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_sms_mark'),
        '短信': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sms_mark'),
        'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
        'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
        'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
        'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
        'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
        '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
        '拍照': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
        '名片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
        'GIF': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_gif'),
        '更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
        'com.chinasofti.rcs:id/input_divider_inside': (MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
        'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
        'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
        '说点什么': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
        '发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
        'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
        'com.chinasofti.rcs:id/ib_audio': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
        'com.chinasofti.rcs:id/ib_record_red_dot': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_record_red_dot'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击设置')
    def click_setting(self):
        self.click_element(self.__locators['设置'])

    @TestLogger.log('输入消息文本')
    def input_message_text(self, content):
        self.input_text(self.__locators['说点什么'], content)

    @TestLogger.log('点击发送按钮')
    def click_send_button(self):
        self.click_element(self.__locators['发送按钮'])

    @TestLogger.log('发送消息')
    def send_message(self, content):
        self.input_message_text(content)
        self.click_send_button()

    @TestLogger.log('发送图片')
    def send_img_msgs(self, name_order_mapper):
        """
        发送图片、视频消息
        :return:
        """
        self.click_element(self.__locators['照片'])
        self.select_and_send_in_img_selector(name_order_mapper)

    @TestLogger.log('检查是否收到期望的消息内容')
    def assert_message_content_display(self, content, max_wait_time=5):
        try:
            self.wait_until(
                lambda d: self.is_text_present(content),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('聊天界面没有收到消息：{}'.format(content))
