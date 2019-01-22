from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SearchOfficialAccountPage(BasePage):
    """搜索公众号"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountSearchNewActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/relativeLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/relativeLayout'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '搜索公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
        '清空关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '公众号列表': (MobileBy.ID, 'com.chinasofti.rcs:id/single_result_list'),
        '公众号': (MobileBy.XPATH,
                '//*[@resource-id="com.chinasofti.rcs:id/single_result_list"]/*[//*['
                '@resource-id="com.chinasofti.rcs:id/item_layout"]]'),
        '公众号头像': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_user_photo'),
        '公众号名称': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_name'),
        '公众号描述': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_info'),
        '关注/已关注': (MobileBy.ID, 'com.chinasofti.rcs:id/button_subscribe'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('输入搜索关键字')
    def input_search_key(self, key):
        self.input_text(self.__locators['搜索公众号'], key + '\n')

    @TestLogger.log('清空搜索关键字')
    def clear_search_key(self):
        self.click_element(self.__locators['清空关键字'])

    @TestLogger.log('关注搜索结果前N个公众号')
    def subscribe_first_items(self, amount):
        """
        关注列表序号amount之前的公众号
        :param amount: 总数
        :return:
        """
        sum = 0
        for rs in self.mobile.list_iterator(self.__locators['公众号列表'], self.__locators['公众号']):
            self.subscribe_official_account(rs)
            sum += 1
            if sum >= amount:
                return sum

    @TestLogger.log('判断公众号是否已关注')
    def is_official_account_subscribed(self, locator):
        """
        判断公众号是否已关注
        :param locator: 公众号跟节点定位器 OR 公众号跟节点元素
        :return: True=已关注，False=未关注
        """
        from appium.webdriver import WebElement
        if isinstance(locator, (list, tuple)):
            account = self.get_element(locator)
        elif isinstance(locator, WebElement):
            account = locator
        else:
            raise ValueError('传入参数类型不正确')

        state = account.find_element(*self.__locators['关注/已关注'])
        return state in ['已关注']

    @TestLogger.log('关注公众号')
    def subscribe_official_account(self, locator):
        """
        关注公众号
        :param locator: 公众号跟节点定位器 OR 公众号跟节点元素
        :return:
        """
        from appium.webdriver import WebElement
        if isinstance(locator, (list, tuple)):
            account = self.get_element(locator)
        elif isinstance(locator, WebElement):
            account = locator
        else:
            raise ValueError('传入参数类型不正确')

        state = account.find_element(*self.__locators['关注/已关注'])
        if state in ['关注']:
            state.click()
