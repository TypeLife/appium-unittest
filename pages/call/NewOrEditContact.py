from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class NewOrEditContactPage(BasePage):
    """新建或者编辑联系人"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.NewOrEditContactActivity'

    __locators = {'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/iv_back': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  '新建联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
                  '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save_or_sure'),
                  'com.chinasofti.rcs:id/item_name': (MobileBy.ID, 'com.chinasofti.rcs:id/item_name'),
                  '姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv'),
                  '输入姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/et'),
                  'com.chinasofti.rcs:id/view': (MobileBy.ID, 'com.chinasofti.rcs:id/view'),
                  'com.chinasofti.rcs:id/item_number': (MobileBy.ID, 'com.chinasofti.rcs:id/item_number'),
                  '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv'),
                  '输入号码': (MobileBy.ID, 'com.chinasofti.rcs:id/et'),
                  'com.chinasofti.rcs:id/view51ecb9dc-0298-4b1a-b5a6-4465ff0b0753': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/view'),
                  'com.chinasofti.rcs:id/item_company': (MobileBy.ID, 'com.chinasofti.rcs:id/item_company'),
                  '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/tv'),
                  '输入公司': (MobileBy.ID, 'com.chinasofti.rcs:id/et'),
                  'com.chinasofti.rcs:id/view45a79373-7b85-4c42-8d08-843e1e636bf3': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/view'),
                  'com.chinasofti.rcs:id/item_job': (MobileBy.ID, 'com.chinasofti.rcs:id/item_job'),
                  '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/tv'),
                  "确定删除": (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button2'),
                  "删除联系人": (MobileBy.ID, "com.chinasofti.rcs:id/tv_delete_contact")
                  }

    @TestLogger.log()
    def input_name(self, text):
        """输入姓名"""
        self.input_text(self.__locators["输入姓名"], text)

    @TestLogger.log()
    def input_contact_info(self, index, text):
        """输入联系人信息"""
        el = self.get_elements(self.__locators["输入号码"])
        if len(el) > 0:
            el[index].send_keys(text)

    @TestLogger.log()
    def click_save_or_sure(self):
        """点击保存"""
        self.click_element(self.__locators["保存"])

    @TestLogger.log("删除联系人")
    def click_delete_number(self):
        self.click_element(self.__locators['删除联系人'])

    @TestLogger.log("确定删除")
    def click_sure_delete(self):
        """点击返回"""
        self.click_element(self.__locators['确定删除'])
