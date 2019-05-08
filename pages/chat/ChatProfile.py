from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatProfilePage(BasePage):
    """聊天名片页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/top_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/top_layout'),
                  'com.chinasofti.rcs:id/layout_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_search'),
                  '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  'com.chinasofti.rcs:id/bottom_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/bottom_layout'),
                  'com.chinasofti.rcs:id/contact_selection_list_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_selection_list_view'),
                  '容器列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
                  'com.chinasofti.rcs:id/local_contacts': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
                  '选择和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
                  'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
                  '联系人列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
                  'com.chinasofti.rcs:id/asp_selecttion_contact_content': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/asp_selecttion_contact_content'),
                  'D': (MobileBy.ID, ''),
                  '左侧字母': (MobileBy.ID, 'com.chinasofti.rcs:id/index_text'),
                  'dx1645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '15338821645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'F': (MobileBy.ID, ''),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '18681151872': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'H': (MobileBy.ID, ''),
                  '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '12560': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'W': (MobileBy.ID, ''),
                  '王者': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '14775290412': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'X': (MobileBy.ID, ''),
                  '小刘': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '14775290418': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'xzq': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  '索引字母容器': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  'Y': (MobileBy.ID, ''),
                  'Z': (MobileBy.ID, ''),

                  # 个人名片页面
                  '_android:id/content': (MobileBy.ID, 'android:id/content'),
                  '取消发送名片': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_img'),
                  'com.chinasofti.rcs:id/head_card_img': (MobileBy.ID, 'com.chinasofti.rcs:id/head_card_img'),
                  '_frank': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
                  '_18681151872': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
                  '发送名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv')
                  }

    def get_left_letters(self):
        """获取左侧字母"""
        els = self.get_elements(self.__class__.__locators['左侧字母'])
        if not els:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        letters = []
        for el in els:
            letters.append(el.text)
        return letters

    def get_letters_index(self):
        """获取所有索引字母"""
        container_el = self.get_element(self.__class__.__locators['索引字母容器'])
        letter_els = container_el.find_elements(MobileBy.XPATH, "//android.widget.TextView")
        if not letter_els:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        letters = []
        for el in letter_els:
            letters.append(el.text)
        return letters

    @TestLogger.log()
    def click_letter_index(self, letter):
        """点击字母索引"""
        container_el = self.get_element(self.__class__.__locators['索引字母容器'])
        container_el.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='%s']" % letter).click()

    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_direction(self.__class__.__locators['容器列表'], 'up')

    def get_first_page_contacts_name(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
            return contacts_name
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")

    @TestLogger.log()
    def get_contacts_name(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        flag = True
        current = 0
        while flag:
            current += 1
            if current > 20:
                return
            self.page_up()
            els = self.get_elements(self.__class__.__locators["联系人名"])
            for el in els:
                if el.text not in contacts_name:
                    contacts_name.append(el.text)
                else:
                    flag = False
        return contacts_name

    @TestLogger.log()
    def select_card(self):
        """选择名片"""
        # els = self.get_elements(self.__class__.__locators["联系人名"])
        els = self.get_elements(self.__class__.__locators["联系人列表"])
        if els:
            els[0].click()
            return True
        return False

    @TestLogger.log()
    def send_card(self):
        """发送名片"""
        self.click_element(self.__class__.__locators['发送名片'])
        time.sleep(5)

    @TestLogger.log()
    def cancel_send_card(self):
        """取消发送名片"""
        self.click_element(self.__class__.__locators['取消发送名片'])

    @TestLogger.log()
    def wait_for_card_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待名片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发送名片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待聊天名片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def search(self, condition):
        """搜索联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], condition)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
