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
                  '重发按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '重发消息确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '语音消息体': (MobileBy.ID, 'com.chinasofti.rcs:id/img_audio_play_icon'),
                  '位置返回': (MobileBy.ID, 'com.chinasofti.rcs:id/location_back_btn'),
                  '表情按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '表情页': (MobileBy.ID, 'com.chinasofti.rcs:id/gv_expression'),
                  '表情': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_expression_image'),
                  '输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  '关闭表情页': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression_keyboard'),
                  '多选返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '多选计数': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_count'),
                  '多选选择框': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_check'),
                  '多选删除': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_delete'),
                  '多选转发': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_forward'),
                  '删除已选信息': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '取消删除已选信息': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                  "返回上一级": (MobileBy.ID, "com.chinasofti.rcs:id/left_back")
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

    @TestLogger.log()
    def is_exist_msg_send_failed_button(self):
        """判断是否有重发按钮"""
        el = self.get_elements(self.__locators['重发按钮'])
        return len(el) > 0

    @TestLogger.log()
    def click_msg_send_failed_button(self):
        """点击重发按钮"""
        self.click_element(self.__class__.__locators["重发按钮"])

    @TestLogger.log()
    def click_resend_confirm(self):
        """点击重发消息确定"""
        self.click_element(self.__class__.__locators["重发消息确定"])

    @TestLogger.log()
    def click_clean_video(self):
        """点击删除消息视频"""
        try:
            el = self.get_element(self.__class__.__locators["消息视频"])
            self.press(el)
            self.click_element(self.__class__.__locators["删除"])
        except:
                pass
        return self

    @TestLogger.log()
    def press_voice_message_to_do(self,text):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def get_width_of_msg_of_text(self):
        """获取文本信息框的大小"""
        el=self.get_element((MobileBy.ID,'com.chinasofti.rcs:id/tv_message'))
        rect=el.rect
        return rect["width"]

    @TestLogger.log()
    def is_call_page_load(self):
        """判断是否可以发起呼叫"""
        el = self.get_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def click_end_call_button(self):
        """点击结束呼叫按钮 """
        self.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @TestLogger.log()
    def click_location_back(self):
        """点击位置页面返回 """
        self.click_element(self.__class__.__locators['位置返回'])

    @TestLogger.log()
    def click_expression_button(self):
        """点击表情按钮"""
        self.click_element(self.__class__.__locators["表情按钮"])

    @TestLogger.log()
    def is_exist_expression_page(self):
        """是否存在表情页"""
        return self._is_element_present(self.__class__.__locators["表情页"])

    @TestLogger.log()
    def click_expression_page_close_button(self):
        """点击表情页关闭"""
        self.click_element(self.__class__.__locators["关闭表情页"])

    @TestLogger.log()
    def get_expressions(self):
        """获取表情包"""
        els = self.get_elements(self.__locators['表情'])
        return els

    @TestLogger.log()
    def get_input_box(self):
        """获取输入框"""
        el = self.get_element(self.__locators['输入框'])
        return el

    @TestLogger.log()
    def is_enabled_of_send_button(self):
        """发送按钮状态"""
        flag = self._is_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'))
        return flag

    @TestLogger.log()
    def is_exist_multiple_selection_back(self):
        """是否存在多选【×】关闭按钮"""
        return self._is_element_present(self.__class__.__locators["多选返回"])

    @TestLogger.log()
    def is_exist_multiple_selection_count(self):
        """是否存在多选计数"""
        return self._is_element_present(self.__class__.__locators["多选计数"])

    @TestLogger.log()
    def get_multiple_selection_select_box(self):
        """获取多选选择框"""
        els=self.get_elements(self.__class__.__locators["多选选择框"])
        if els:
            return els
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def is_enabled_multiple_selection_delete(self):
        """判断多选删除是否高亮展示"""
        return self._is_enabled(self.__class__.__locators["多选删除"])

    @TestLogger.log()
    def is_enabled_multiple_selection_forward(self):
        """判断多选转发是否高亮展示"""
        return self._is_enabled(self.__class__.__locators["多选转发"])

    @TestLogger.log()
    def click_multiple_selection_back(self):
        """点击多选返回"""
        self.click_element(self.__class__.__locators["多选返回"])

    @TestLogger.log()
    def is_exist_multiple_selection_select_box(self):
        """是否存在多选选择框"""
        return self._is_element_present(self.__class__.__locators["多选选择框"])

    @TestLogger.log()
    def click_multiple_selection_delete(self):
        """点击多选删除"""
        self.click_element(self.__class__.__locators["多选删除"])

    @TestLogger.log()
    def click_multiple_selection_delete_cancel(self):
        """点击取消删除已选信息"""
        self.click_element(self.__class__.__locators["取消删除已选信息"])

    @TestLogger.log()
    def click_multiple_selection_delete_sure(self):
        """点击确定删除已选信息"""
        self.click_element(self.__class__.__locators["删除已选信息"])

    @TestLogger.log()
    def click_multiple_selection_forward(self):
        """点击多选转发"""
        self.click_element(self.__class__.__locators["多选转发"])

    @TestLogger.log()
    def press_audio_to_do(self,text):
        """长按语音消息体进行操作"""
        els = self.get_elements(self.__class__.__locators["语音消息体"])
        if els:
            self.press(els[0])
            self.click_element(self.__class__.__locators[text])
        else:
            raise AssertionError("没有找到语音消息体")

    @TestLogger.log()
    def get_group_name(self):
        """在群聊页面获取群聊名称"""
        return self.get_element(self.__class__.__locators['群聊001(2)']).text

    @TestLogger.log()
    def get_multiple_selection_count(self):
        """获取多选计数框"""
        el = self.get_element(self.__class__.__locators["多选计数"])
        if el:
            return el
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def press_voice_message(self):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)

    @TestLogger.log()
    def click_return(self):
        """返回上一级"""
        self.click_element(self.__class__.__locators["返回上一级"])

