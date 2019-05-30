import operator
import re
import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class Massassistant(BasePage):
    """群发助手页面"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.GroupSMSEditActivity'

    __locators = {
        #引导页
        '欢迎使用群发助手': (MobileBy.ID, 'com.chinasofti.rcs:id/group_mass_title'),
        '以后再说': (MobileBy.ID, 'com.chinasofti.rcs:id/cancel_btn'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/confirm_btn'),
        '群发助手使用须知': (MobileBy.ID, 'com.chinasofti.rcs:id/group_mass_notify'),
        '': (MobileBy.ID, ''),

        #群发助手页面
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '标题': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
        '收件人': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_sendee'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/select_sendee'),
        '你正在使用群发短信': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_isFree'),
        '?': (MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'),
        '发送短信': (MobileBy.ID, 'com.chinasofti.rcs:id/et_edit'),
        '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send'),

        #跳转到群发助手历史记录页
        '时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
        '记录内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        '记录收件人': (MobileBy.ID, 'com.chinasofti.rcs:id/sendeeNameText'),
        '记录列表': (MobileBy.ID, 'com.chinasofti.rcs:id/context_view'),
        '新增': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_normal_edit'),

    }

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        if self._is_element_present(self.__class__.__locators['确定']):
            self.click_element(self.__class__.__locators['确定'])
        time.sleep(2)

    @TestLogger.log()
    def click_contact_avatar(self):
        """点击选择联系人"""
        self.click_element(self.__class__.__locators['头像'])

    @TestLogger.log()
    def click_input_box(self):
        """点击输入框"""
        self.click_element(self.__class__.__locators['发送短信'])

    @TestLogger.log()
    def input_search_keyword(self,text):
        """输入内容"""
        self.input_text(self.__class__.__locators['发送短信'],text)

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators['发送'])

    @TestLogger.log()
    def check_element_is_clickable(self,locator='发送'):
        """元素是否可点击"""
        return self._is_clickable(self.__class__.__locators[locator])

    @TestLogger.log()
    def page_contain_element(self,locator='新增'):
        """页面应该包含元素检查"""
        return self.page_should_contain_element(self.__class__.__locators[locator])

    @TestLogger.log()
    def input_text_and_send(self,text):
        self.click_input_box()
        time.sleep(1)
        self.input_search_keyword(text)
        time.sleep(1)
        self.click_send()
