from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class NameCardPreviewPage(BasePage):
    """名片预览"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/cancle_img': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_img'),
        'com.chinasofti.rcs:id/head_card_img': (MobileBy.ID, 'com.chinasofti.rcs:id/head_card_img'),
        '安德森': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
        '19876283465': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
        'com.chinasofti.rcs:id/info_ll': (MobileBy.ID, 'com.chinasofti.rcs:id/info_ll'),
        'com.chinasofti.rcs:id/company_ll': (MobileBy.ID, 'com.chinasofti.rcs:id/company_ll'),
        'com.chinasofti.rcs:id/company_image': (MobileBy.ID, 'com.chinasofti.rcs:id/company_image'),
        '中科院': (MobileBy.ID, 'com.chinasofti.rcs:id/company_tv'),
        'com.chinasofti.rcs:id/position_ll': (MobileBy.ID, 'com.chinasofti.rcs:id/position_ll'),
        'com.chinasofti.rcs:id/position_image': (MobileBy.ID, 'com.chinasofti.rcs:id/position_image'),
        '人类文明发展研究院院士': (MobileBy.ID, 'com.chinasofti.rcs:id/position_tv'),
        'com.chinasofti.rcs:id/email_ll': (MobileBy.ID, 'com.chinasofti.rcs:id/email_ll'),
        'com.chinasofti.rcs:id/email_image': (MobileBy.ID, 'com.chinasofti.rcs:id/email_image'),
        'goodmorning@mm.edu': (MobileBy.ID, 'com.chinasofti.rcs:id/email_tv'),
        '发送名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv')
    }

    @TestLogger.log('点击空白关闭名片')
    def click_blank_space(self):
        self.mobile.click_out_side_of_element(self.__locators['android:id/content'])

    @TestLogger.log('点击关闭icon')
    def click_cancel_icon(self):
        self.mobile.click_element(self.__locators['com.chinasofti.rcs:id/cancle_img'])

    @TestLogger.log('发送名片')
    def click_send_name_card(self):
        self.click_element(self.__locators['发送名片'])

    @TestLogger.log('勾选公司字段')
    def check_company_field(self):
        state = self.get_name_card_fields_checked_status().get('company')
        if state is None:
            raise NoSuchElementException('名片上没有找到公司字段')
        elif not state:
            self.click_element(self.__locators['com.chinasofti.rcs:id/company_ll'])

    @TestLogger.log('取消勾选公司字段')
    def uncheck_company_field(self):
        state = self.get_name_card_fields_checked_status().get('company')
        if state is None:
            raise NoSuchElementException('名片上没有找到公司字段')
        elif state:
            self.click_element(self.__locators['com.chinasofti.rcs:id/company_ll'])

    @TestLogger.log('勾选职位字段')
    def check_position_field(self):
        state = self.get_name_card_fields_checked_status().get('position')
        if state is None:
            raise NoSuchElementException('名片上没有找到职位字段')
        elif not state:
            self.click_element(self.__locators['com.chinasofti.rcs:id/position_ll'])

    @TestLogger.log('取消勾选职位字段')
    def uncheck_position_field(self):
        state = self.get_name_card_fields_checked_status().get('position')
        if state is None:
            raise NoSuchElementException('名片上没有找到职位字段')
        elif state:
            self.click_element(self.__locators['com.chinasofti.rcs:id/position_ll'])

    @TestLogger.log('勾选邮箱字段')
    def check_email_field(self):
        state = self.get_name_card_fields_checked_status().get('email')
        if state is None:
            raise NoSuchElementException('名片上没有找到邮箱字段')
        elif not state:
            self.click_element(self.__locators['com.chinasofti.rcs:id/email_ll'])

    @TestLogger.log('取消勾选邮箱字段')
    def uncheck_email_field(self):
        state = self.get_name_card_fields_checked_status().get('email')
        if state is None:
            raise NoSuchElementException('名片上没有找到邮箱字段')
        elif state:
            self.click_element(self.__locators['com.chinasofti.rcs:id/email_ll'])

    @TestLogger.log('获取可选字段的选中状态')
    def get_name_card_fields_checked_status(self):
        unchecked_color = (255, 255, 255, 255)
        company = self.mobile.get_elements(self.__locators['com.chinasofti.rcs:id/company_ll'])
        position = self.mobile.get_elements(self.__locators['com.chinasofti.rcs:id/position_ll'])
        email = self.mobile.get_elements(self.__locators['com.chinasofti.rcs:id/email_ll'])
        optional_fields_checked_state = dict(
            company=None,
            position=None,
            email=None
        )
        if company:
            check_box = company[0].find_element(*self.__locators['com.chinasofti.rcs:id/company_image'])
            color = self.mobile.get_coordinate_color_of_element(check_box, 50, 20, True)
            optional_fields_checked_state['company'] = (color != unchecked_color)
        if position:
            check_box = position[0].find_element(*self.__locators['com.chinasofti.rcs:id/position_image'])
            color = self.mobile.get_coordinate_color_of_element(check_box, 50, 20, True)
            optional_fields_checked_state['position'] = (color != unchecked_color)
        if email:
            check_box = email[0].find_element(*self.__locators['com.chinasofti.rcs:id/email_image'])
            color = self.mobile.get_coordinate_color_of_element(check_box, 50, 20, True)
            optional_fields_checked_state['email'] = (color != unchecked_color)
        print(optional_fields_checked_state)
        return optional_fields_checked_state
