from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class BuildGroupChatPage(Keyboard, BasePage):
    """创建群聊"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '群聊名称': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '为你的群创建一个群名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_expanded'),
        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/et_group_name'),
        '群聊名删除按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_del'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击确定')
    def click_ok(self):
        self.click_element(self.__locators['确定'])

    @TestLogger.log('清空群聊名称')
    def click_clear_button(self):
        self.click_element(self.__locators['群聊名删除按钮'])

    @TestLogger.log('输入群聊名称')
    def input_group_chat_name(self, name):
        self.input_text(self.__locators['群聊'], name)

    @TestLogger.log('创建群聊')
    def create_group_chat(self, name):
        self.hide_keyboard_if_display()
        self.click_clear_button()
        self.hide_keyboard_if_display()
        self.input_group_chat_name(name)
        self.hide_keyboard_if_display()
        self.click_ok()

    def is_enabled_tv_sure(self):
        """判断确定按钮是否可用"""
        return self._is_enabled(self.__locators['确定'])

