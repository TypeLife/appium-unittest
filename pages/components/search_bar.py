from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SearchBar(BasePage):
    """无结果"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.SearchActivity'

    __locators = {
        '输入关键词快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        '删除关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect01'),
        '无结果更换关键词重试': (MobileBy.ID, 'com.chinasofti.rcs:id/no_search_result'),
        '搜索群组': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),


    }

    @TestLogger.log('输入搜索关键字')
    def input_search_keyword(self, keyword):
        """输入搜索关键字"""
        self.input_text(self.__locators['输入关键词快速搜索'], keyword)

    @TestLogger.log('搜索')
    def input_search_hint(self, keyword):
        """搜索"""
        self.input_text(self.__locators['搜索'], keyword)

    @TestLogger.log('搜索群组')
    def click_search_group_hint(self):
        """搜索群组"""
        self.click_element(self.__class__.__locators["搜索群组"])

    @TestLogger.log('点击删除按钮清空搜索框')
    def click_clear_keyword_button(self):
        self.click_element(self.__locators['删除关键字'])

    @TestLogger.log('检查当前搜索框内容')
    def assert_current_search_keyword_is(self, keyword):
        """检查当前搜索框内容"""
        self.element_text_should_be(self.__locators['输入关键词快速搜索'], keyword)

    @TestLogger.log("检查无搜索结果提示语是否显示")
    def assert_no_result_tips_display(self):
        tips_text = '无结果，更换关键词重试'
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['无结果更换关键词重试']) == tips_text
            )
        except TimeoutException:
            raise AssertionError('页面没有出现“{}”提示语'.format(tips_text))
