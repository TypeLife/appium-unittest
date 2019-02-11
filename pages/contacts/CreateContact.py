from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class CreateContactPage(Keyboard, BasePage):
    """新建联系人"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.NewContactActivity'

    __locators = {
        '返回': (MobileBy.XPATH, '//*[contains(@resource-id, "back")]'),
        '新建联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save_or_sure'),

        '姓名': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_name"]//android.widget.TextView'),
        '输入姓名': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_name"]//android.widget.EditText'),

        '电话': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_number"]//android.widget.TextView'),
        '输入号码': (MobileBy.XPATH,'//*[@resource-id="com.chinasofti.rcs:id/item_number"]//android.widget.EditText'),

        '公司': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_company"]//android.widget.TextView'),
        '输入公司': (MobileBy.XPATH,'//*[@resource-id="com.chinasofti.rcs:id/item_company"]//android.widget.EditText'),

        '职位':(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_job"]//android.widget.TextView'),
        '输入职位': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_job"]//android.widget.EditText'),

        '邮箱': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_email"]//android.widget.TextView'),
        '输入邮箱': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_email"]//android.widget.EditText'),
    }

    @TestLogger.log('输入姓名')
    def input_name(self, name):
        self.input_text(self.__locators['输入姓名'], name)

    @TestLogger.log('输入号码')
    def input_number(self, name):
        self.input_text(self.__locators['输入号码'], name)

    @TestLogger.log('输入公司')
    def input_company(self, name):
        self.input_text(self.__locators['输入公司'], name)

    @TestLogger.log('输入职位')
    def input_position(self, name):
        self.input_text(self.__locators['输入职位'], name)

    @TestLogger.log('输入邮箱')
    def input_email_address(self, name):
        self.input_text(self.__locators['输入邮箱'], name)

    @TestLogger.log('点击保存')
    def save_contact(self):
        self.click_element(self.__locators['保存'])

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('创建联系人')
    def create_contact(self, name, number, company='', position='', email=''):
        if name:
            self.hide_keyboard_if_display()
            self.input_name(name)
        if number:
            self.hide_keyboard_if_display()
            self.input_number(number)
        if company:
            self.hide_keyboard_if_display()
            self.input_company(company)
        if position:
            self.hide_keyboard_if_display()
            self.input_position(position)
        if email:
            self.hide_keyboard_if_display()
            self.input_email_address(email)
        self.hide_keyboard_if_display()
        self.save_contact()

    @TestLogger.log('等待页面加载')
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['输入姓名'])
        )
