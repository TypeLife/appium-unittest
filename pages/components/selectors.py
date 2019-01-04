from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ContactsSelector(BasePage):
    """
    联系人选择器：
        标签分组-添加联系人
    """
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
        'com.chinasofti.rcs:id/contact_selection_list_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_selection_list_view'),
        '联系人列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
        '联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        '选择和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
        'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
        'com.chinasofti.rcs:id/asp_selecttion_contact_content': (
            MobileBy.ID, 'com.chinasofti.rcs:id/asp_selecttion_contact_content'),
        'G': (MobileBy.ID, ''),
        'com.chinasofti.rcs:id/select_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/select_icon'),
        '联系人名称': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        'H': (MobileBy.ID, ''),
        '字母导航栏': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container')
    }

    @TestLogger.log('选择本地联系人')
    def select_local_contacts(self, *name_list):
        name_list = list(name_list)

        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['搜索或输入手机号'])
        )
        for cont in self.mobile.list_iterator(self.__locators['联系人列表'], self.__locators['联系人']):
            name = cont.find_element(*self.__locators['联系人名称']).text
            if name in name_list:
                cont.click()
                name_list.remove(name)
            if not name_list:
                break

        self.click_ok_button()
        if name_list:
            print('没有找到以下联系人：{}'.format(name_list))
            return False
        return True

    @TestLogger.log('点击确定')
    def click_ok_button(self):
        self.click_element(self.__locators['确定'])

    @TestLogger.log('检查点：输入框文案="搜索或输入手机号"')
    def assert_contacts_selector_search_box_place_holder_is_right(self):
        self.mobile.assert_element_text_should_be(self.__locators['搜索或输入手机号'], '搜索或输入手机号')

    @TestLogger.log('检查点：页面标题="选择联系人"')
    def assert_contacts_selector_page_title_is_right(self):
        self.mobile.assert_element_text_should_be(self.__locators['选择联系人'], '选择联系人')

    @TestLogger.log('检查点：右上角显示确定按钮')
    def assert_contacts_selector_page_display_ok_button(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['确定'])

    @TestLogger.log('检查点：页面包含文本')
    def assert_contacts_selector_page_contains_text(self, text):
        self.mobile.assert_screen_contain_text(text)

    @TestLogger.log('检查点：右边显示字母导航')
    def assert_contacts_selector_page_contains_alphabet_nav(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['字母导航栏'])
