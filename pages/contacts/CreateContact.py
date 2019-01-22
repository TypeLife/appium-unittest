from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class CreateContactPage(Keyboard, BasePage):
    """新建联系人"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.NewContactActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/contact_new_common': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_new_common'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back_btn_new'),
        '新建联系人': (MobileBy.ID, ''),
        'com.chinasofti.rcs:id/edit_new': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_new'),
        '完成': (MobileBy.ID, 'com.chinasofti.rcs:id/complete_tv'),
        '姓名   *': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
        '输入姓名': (MobileBy.XPATH, '//*[contains(@resource-id,"contact_name")]'),
        'com.chinasofti.rcs:id/view1': (MobileBy.ID, 'com.chinasofti.rcs:id/view1'),
        '电话   *': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
        '输入号码': (MobileBy.XPATH, '//*[contains(@resource-id,"contact_phone")]'),
        'com.chinasofti.rcs:id/view2': (MobileBy.ID, 'com.chinasofti.rcs:id/view2'),
        'com.chinasofti.rcs:id/ll_company': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_company'),
        '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/company_tv'),
        '输入公司': (MobileBy.XPATH, '//*[contains(@resource-id,"contact_company")]'),
        'com.chinasofti.rcs:id/view3': (MobileBy.ID, 'com.chinasofti.rcs:id/view3'),
        'com.chinasofti.rcs:id/ll_job': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_job'),
        '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/job_tv'),
        '输入职位': (MobileBy.XPATH, '//*[contains(@resource-id,"contact_job")]'),
        'com.chinasofti.rcs:id/view4': (MobileBy.ID, 'com.chinasofti.rcs:id/view4'),
        'com.chinasofti.rcs:id/ll_email': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_email'),
        '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/email_tv'),
        '输入邮箱': (MobileBy.XPATH, '//*[contains(@resource-id,"contact_email")]'),
        'com.chinasofti.rcs:id/view5': (MobileBy.ID, 'com.chinasofti.rcs:id/view5'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
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

    @TestLogger.log('点击完成')
    def save_contact(self):
        self.click_element(self.__locators['完成'])

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
