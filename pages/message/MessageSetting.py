from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class MessageSettingPage(BasePage):
    """聊天设置"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.PcMessageSettingActivity'

    __locators = {
        '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
        '消息免打扰': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_undisturb'),
        '置顶聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
    }

    def enter_serarch_chat_recor(self):
        """点击查找聊天内容"""
        self.click_element(self.__class__.__locators["查找聊天内容"])

    def click_bak(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
