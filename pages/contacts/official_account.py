from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class OfficialAccountPage(BasePage):
    """公众号"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountsListActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
        '加号': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_add_btn'),
        '订阅/服务号': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_tab_title" and @text="订阅/服务号"]'),
        '企业号': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_tab_title" and @text="企业号"]'),
        '公众号列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '公众号列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView"]/*'),
        '公众号头像': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_user_photo'),
        '公众号名称': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_name'),
        '公众号描述': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_info'),
        '未关注任何企业号': (MobileBy.ID, 'com.chinasofti.rcs:id/empty_hint_view'),
    }

    @TestLogger.log('点击添加')
    def click_add(self):
        self.click_element(self.__locators['加号'])

    @TestLogger.log('点击tag标签')
    def click_tag(self, tag_name):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/tv_tab_title" and @text="{}"]'.format(tag_name)]
        self.click_element(locator)

    @TestLogger.log('检查企业号列表是否为空')
    def assert_enterprise_account_list_is_empty(self):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['未关注任何企业号'])
            )
            self.element_text_should_be(
                self.__locators['未关注任何企业号'],
                '未关注任何企业号', '检查点：列表为空时显示默认文案：未关注任何企业号'
            )
        except TimeoutException:
            raise AssertionError("检查点：企业号列表为空")

    @TestLogger.log()
    def select_one_account_by_name(self, name):
        """通过名称选择一个公众号"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/textview_user_name" and @text ="%s"]' % name))
