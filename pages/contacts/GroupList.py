from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupListPage(BasePage):
    """群组列表"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListActivity2'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '新建群组': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_add_btn'),
        '搜索群组': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search_bar'),
        'com.chinasofti.rcs:id/fragment_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fragment_container'),
        '群列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        '列表项首字母': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '滚动条字符': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/*'),
    }

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击创建群')
    def click_create_group(self):
        self.click_element(self.__locators['新建群组'])

    @TestLogger.log('搜索群')
    def click_search_input(self):
        self.click_element(self.__locators['搜索群组'])

    @TestLogger.log('判断列表是否存在群XXX')
    def is_group_in_list(self, name):
        groups = self.mobile.list_iterator(self.__locators['群列表'], self.__locators['列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH,
                                   '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('点击群')
    def click_group(self, name):
        if self.is_group_in_list(name):
            self.click_element((MobileBy.XPATH,
                                '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                '@text="{}"]'.format(name)))
        else:
            raise NoSuchElementException('找不到群：{}'.format((MobileBy.XPATH,
                                                           '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                                           '@text="{}"]'.format(name))))
