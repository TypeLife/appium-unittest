from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupListSearchPage(BasePage):
    """搜索群组"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatSearchActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '输入关键字搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
        '删除关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_clear'),
        '搜索结果列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView"]/*'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/title_ll'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('输入搜索关键字')
    def input_search_keyword(self, keyword):
        self.input_text(self.__locators['输入关键字搜索'], keyword)

    @TestLogger.log('清空搜索关键字')
    def clear_search_keyword(self):
        self.click_element(self.__locators['删除关键字'])

    @TestLogger.log('查看是否显示XX群')
    def is_group_in_list(self, name):
        groups = self.mobile.list_iterator(self.__locators['搜索结果列表'], self.__locators['列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('点击群组')
    def click_group(self, name):
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                            '@text="{}"]'.format(name)))

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在搜索群组"""
        el = self.get_elements(self.__locators['群聊'])
        if len(el) > 0:
            return True
        return False