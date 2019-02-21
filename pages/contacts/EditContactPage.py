from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EditContactPage(BasePage):
    """编辑联系人页"""

    ACTIVITY = 'com.cmicc.module_contact.activitys.NewOrEditContactActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '编辑联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save_or_sure'),
        '删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_delete_contact'),
        '取消删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button1'),
        '确定删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button2'),
    }

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