from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard
import time


class EditContactPage(Keyboard, BasePage):
    """编辑联系人页"""

    ACTIVITY = 'com.cmicc.module_contact.activitys.NewOrEditContactActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '编辑联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save_or_sure'),
        '删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_delete_contact'),
        '取消删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button1'),
        '确定删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button2'),

        '姓名': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_name"]//android.widget.TextView'),
        '输入姓名': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_name"]//android.widget.EditText'),

        '电话': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_nu mber"]//android.widget.TextView'),
        '输入号码': (MobileBy.XPATH,'//*[@resource-id="com.chinasofti.rcs:id/item_number"]//android.widget.EditText'),

        '公司': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_company"]//android.widget.TextView'),
        '输入公司': (MobileBy.XPATH,'//*[@resource-id="com.chinasofti.rcs:id/item_company"]//android.widget.EditText'),

        '职位':(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_job"]//android.widget.TextView'),
        '输入职位': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_job"]//android.widget.EditText'),

        '邮箱': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_email"]//android.widget.TextView'),
        '输入邮箱': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_email"]//android.widget.EditText'),
        '允许': (MobileBy.XPATH, '//*[@text="允许"]'),
    }

    @TestLogger.log("点击允许权限")
    def click_allow_button(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['允许']):
            self.click_element(self.__class__.__locators['允许'])
        return True

    @TestLogger.log("检查控件是否为某个文字")
    def check_element_word(self, text='', word=''):
        els = self.get_elements(self.__class__.__locators[text])
        if els and els[0].text == word:
            return True
        return False

    @TestLogger.log('删除联系人')
    def click_delete_contact(self):
        """点击删除联系人"""
        self.click_element(self.__locators['删除联系人'])

    @TestLogger.log('取消删除联系人')
    def click_not_delete(self):
        """取消删除联系人"""
        self.click_element(self.__locators['取消删除联系人'])

    @TestLogger.log('确定删除联系人')
    def click_sure_delete(self):
        """确定删除联系人"""
        self.click_element(self.__locators['确定删除联系人'])

    @TestLogger.log()
    def is_exist_name(self,text):
        """检查姓名的内容"""
        # return self.element_should_contain_text(self.__class__.__locators["姓名"], text)
        return self._is_element_present(self.__class__.__locators["姓名"])

    @TestLogger.log()
    def is_exist_phone(self,text):
        """检查电话内容"""
        # return self.element_should_contain_text(self.__class__.__locators["电话"], text)
        return self._is_element_present(self.__class__.__locators["电话"])

    @TestLogger.log('点击确定')
    def click_ensure(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log('点击输入姓名')
    def click_input_name(self):
        """点击输入姓名"""
        self.click_element(self.__locators['输入姓名'])

    @TestLogger.log('输入姓名')
    def input_name(self, name):
        """输入姓名"""
        self.input_text(self.__locators['输入姓名'], name)

    @TestLogger.log('点击输入号码')
    def click_input_number(self):
        """点击输入号码"""
        self.click_element(self.__locators['输入号码'])

    @TestLogger.log('输入号码')
    def input_number(self, name):
        """输入号码"""
        self.input_text(self.__locators['输入号码'], name)

    @TestLogger.log('输入公司')
    def input_company(self, name):
        self.input_text(self.__locators['输入公司'], name)

    @TestLogger.log('输入公司号码')
    def input_company(self, name):
        self.input_text(self.__locators['输入公司'], name)

    @TestLogger.log('输入职位')
    def input_position(self, name):
        self.input_text(self.__locators['输入职位'], name)

    @TestLogger.log('输入邮箱')
    def input_email_address(self, name):
        self.input_text(self.__locators['输入邮箱'], name)

    @TestLogger.log('判断确定按钮是否不可点击')
    def assert_ensure_button_should_not_be_clickable(self):
        if self._is_enabled(self.__locators['确定']):
            raise AssertionError("ensure_button_should_not_be_clickable")

    @TestLogger.log('判断确定按钮是否可点击')
    def assert_ensure_button_should_be_clickable(self):
        if not self._is_enabled(self.__locators['确定']):
            raise AssertionError("ensure_button_should_not_be_clickable")