import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ContactListSearchPage(BasePage):
    """搜索联系人"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.SearchActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/relativeLayout01': (MobileBy.ID, 'com.chinasofti.rcs:id/relativeLayout01'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'),
        '输入关键字搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        '删除关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect01'),
        'com.chinasofti.rcs:id/tablayout': (MobileBy.ID, 'com.chinasofti.rcs:id/tablayout'),
        '本地通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tab_title'),
        '和通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tab_title'),
        'com.chinasofti.rcs:id/result_wrapper': (MobileBy.ID, 'com.chinasofti.rcs:id/result_wrapper'),
        '搜索结果列表': (MobileBy.ID, 'com.chinasofti.rcs:id/single_result_list'),
        '列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/root_view'),
        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
        '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone'),
        '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击分享名片')
    def click_share_card(self):
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log('输入搜索关键字')
    def input_search_keyword(self, keyword):
        self.input_text(self.__locators['输入关键字搜索'], keyword)

    @TestLogger.log('清空搜索关键字')
    def clear_search_keyword(self):
        self.click_element(self.__locators['删除关键字'])

    @TestLogger.log('查看是否显示XX联系人')
    def is_contact_in_list(self, name):
        time.sleep(1)
        groups = self.mobile.list_iterator(self.__locators['搜索结果列表'], self.__locators['列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and ' +
                                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('点击联系人')
    def click_contact(self, name):
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and ' +
                            '@text="{}"]'.format(name)))
