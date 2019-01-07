from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class BaseChatPage(BasePage):
    """聊天基类抽取"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
                  'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
                  '选择图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '选择相机': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
                  '选择名片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  '选择gif': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_gif'),
                  '选择更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '语音按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  '发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
                  'com.chinasofti.rcs:id/ib_record_red_dot': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_record_red_dot'),
                  # 消息长按弹窗
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  # 撤回消息时的弹窗
                  '我知道了': (MobileBy.XPATH, "//*[contains(@text, '我知道了')]"),
                  # 用户须知
                  '用户须知': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
                  '我已阅读': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok'),
                  # 在聊天会话页面点击不可阅读文件时的弹窗
                  '打开方式': (MobileBy.XPATH, "//*[contains(@text, '打开方式')]"),
                  '取消': (MobileBy.ID, 'android:id/button2'),
                  }

    @TestLogger.log()
    def click_i_have_read(self):
        """点击我已阅读"""
        self.click_element(self.__class__.__locators["我已阅读"])
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def collection_file(self, file):
        """收藏文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['收藏'])

    @TestLogger.log()
    def forward_file(self, file):
        """转发文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['转发'])

    @TestLogger.log()
    def delete_mess(self, mess):
        """删除消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)
        self.click_element(self.__class__.__locators['删除'])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators['删除'])

    @TestLogger.log()
    def recall_mess(self, mess):
        """撤回消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log()
    def click_i_know(self):
        """撤回消息时，弹窗处理，点击 我知道了"""
        self.click_element(self.__class__.__locators["我知道了"])

    @TestLogger.log()
    def press_mess(self, mess):
        """长按消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)

    @TestLogger.log()
    def click_pic(self):
        """点击选择图片"""
        self.click_element(self.__class__.__locators["选择图片"])

    @TestLogger.log()
    def click_take_photo(self):
        """点击选择相机"""
        self.click_element(self.__class__.__locators["选择相机"])

    @TestLogger.log()
    def click_gif(self):
        """点击选择gif"""
        self.click_element(self.__class__.__locators["选择gif"])

    @TestLogger.log()
    def click_more(self):
        """点击选择更多 +"""
        self.click_element(self.__class__.__locators["选择更多"])

    @TestLogger.log()
    def input_message(self, message):
        """输入聊天信息"""
        self.input_text(self.__class__.__locators["说点什么..."], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def get_input_message(self):
        """获取输入框的信息"""
        el = self.get_element(self.__class__.__locators["说点什么..."])
        return el.text

    @TestLogger.log()
    def send_message(self):
        """发送聊天信息"""
        self.click_element(self.__class__.__locators["发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def page_should_contain_audio_btn(self):
        """语音按钮检查"""
        self.page_should_contain_element(self.__locators["语音按钮"])

    @TestLogger.log()
    def page_should_contain_send_btn(self):
        """发送按钮检查"""
        self.page_should_contain_element(self.__locators["发送按钮"])

    @TestLogger.log()
    def click_audio_btn(self):
        """点击语音按钮"""
        self.click_element(self.__class__.__locators["语音按钮"])

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_undisturb(self):
        """是否存在消息免打扰标志"""
        return self._is_element_present(self.__class__.__locators["消息免打扰"])

    @TestLogger.log()
    def is_exist_dialog(self, timeout=3, auto_accept_alerts=False):
        """是否存在 用户须知 弹框"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["用户须知"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def open_file_in_chat_page(self, file):
        """在聊天会话页面打开文件"""
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))

    @TestLogger.log()
    def wait_for_open_file(self, timeout=8, auto_accept_alerts=True):
        """等待打开文件页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/menu'))
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_back_in_open_file_page(self):
        """在打开文件页面点击返回"""
        try:
            self.click_element((MobileBy.ID, "com.chinasofti.rcs:id/back"))
        except:
            self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def wait_for_call_sys_app_page(self, timeout=8, auto_accept_alerts=True):
        """等待调起系统应用页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['打开方式'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_cancle(self):
        """点击取消"""
        self.click_element(self.__class__.__locators['取消'])
