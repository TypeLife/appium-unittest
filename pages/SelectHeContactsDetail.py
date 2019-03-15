import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from library.core.utils.applicationcache import current_mobile


class SelectHeContactsDetailPage(BasePage):
    """选择和通讯录联系人页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseContactSelectInnerActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
                  'com.chinasofti.rcs:id/btn_close_actionbar': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_action_bar_title'),
                  'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity'),
                  '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/breadCrumbs_enterprise_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/breadCrumbs_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/breadcrumbs_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/breadcrumbs_layout'),
                  '和通讯录': (MobileBy.ID, 'android:id/title'),
                  'android:id/icon': (MobileBy.ID, 'android:id/icon'),
                  'myteam': (MobileBy.ID, 'android:id/title'),
                  'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity'),
                  'android:id/list': (MobileBy.ID, 'android:id/list'),
                  'com.chinasofti.rcs:id/layout_personal_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_personal_contactlist'),
                  'com.chinasofti.rcs:id/img_icon_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_contactlist'),
                  'com.chinasofti.rcs:id/line_search_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/line_search_contactlist'),
                  'axzq': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '13510772034': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_position_personal_contactlist'),
                  '测试号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '14775290489': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_position_personal_contactlist'),
                  '张三': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
                  'com.chinasofti.rcs:id/line_big_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/line_big_contactlist'),
                  'com.chinasofti.rcs:id/layout_department_contactlist': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/layout_department_contactlist'),
                  'com.chinasofti.rcs:id/img_icon_department': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_department'),
                  '测试一部': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  '部门名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  'com.chinasofti.rcs:id/img_right_department': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/img_right_department'),
                  'com.chinasofti.rcs:id/line_contactlist1': (MobileBy.ID, 'com.chinasofti.rcs:id/line_contactlist1'),
                  # 选择一个和通讯录联系人转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '取消': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '确定': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
                  }

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def select_one_linkman(self, name):
        """选择一个联系人"""
        self.click_element((MobileBy.XPATH, "//*[@text='%s']" % name))

    @TestLogger.log()
    def select_one_department(self, name):
        """选择一个部门"""
        self.click_element((MobileBy.XPATH, "//*[@text='%s']" % name))

    @TestLogger.log()
    def get_contacts_names(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators['联系人名'])
        contacts_names = []
        if els:
            for el in els:
                contacts_names.append(el.text)
        return contacts_names

    @TestLogger.log()
    def get_department_names(self):
        """获取部门名称"""
        els = self.get_elements(self.__class__.__locators['部门名称'])
        department_names = []
        if els:
            for el in els:
                department_names.append(el.text)
        return department_names

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def input_search(self, text):
        """输入名字"""
        self.input_text(self.__locators["搜索"], text)
        time.sleep(2.5)
        current_mobile().hide_keyboard_if_display()

    @TestLogger.log()
    def select_one_he_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name_personal_contactlist" and contains(@text,"%s")]' % name))

    @TestLogger.log()
    def select_one_he_contact_by_number(self, number):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_number_personal_contactlist" and contains(@text,"%s")]' % number))
