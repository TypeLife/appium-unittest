import operator

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EmailAssistantPage(BasePage):
    """139邮箱助手"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MailMsgListActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '139邮箱助手': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
        '消息列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '消息项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        '发送者': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '红点': (MobileBy.ID, 'com.chinasofti.rcs:id/red_dot_silent'),
        '时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '简要信息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
    }

    @TestLogger.log('点击返回上一页图标')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log("检查最新的一条消息的Title")
    def assert_the_first_message_is(self, title, max_wait_time=5):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['发送者'])[
                                    :len(title) if len(title) > 0 else None] == title,
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('{}秒内没有找到"{}"的最新消息'.format(max_wait_time, title))

    @TestLogger.log("点击邮件消息")
    def click_message(self, title):
        # TODO
        # 找到就直接点击
        menu_locator = [MobileBy.XPATH,
                        '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and contains(@text,"{}")]'.format(title)]
        self._find_message(menu_locator)
        self.click_element(menu_locator)

    @TestLogger.log("下一页")
    def page_down(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        self.swipe_by_direction(self.__locators['消息列表'], 'up')

    @TestLogger.log("下一页")
    def page_up(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        self.swipe_by_direction(self.__locators['消息列表'], 'down')

    @TestLogger.log("定位到列表顶部")
    def scroll_to_top(self):
        for p in self._iterate_pages(desc_on=True):
            print(p)

    @TestLogger.log("定位到列表底部")
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        for p in self._iterate_pages(desc_on=False):
            print(p)

    @TestLogger.log()
    def _find_message(self, locator):
        for p in self._iterate_pages(desc_on=True):
            pass
        for p in self._iterate_pages(desc_on=False):
            # print(p)
            if self._is_element_present(locator):
                return
        for p in self._iterate_pages(desc_on=True):
            pass
        try:
            self.wait_until(
                lambda d: self._is_element_present(locator)
            )
        except TimeoutException:
            raise NoSuchElementException('找不到元素：{}'.format(locator))

    def _iterate_pages(self, desc_on=False):
        """
        迭代消息列表,默认从上往下
        :return:
        """
        page_number = 1
        while True:
            yield page_number
            items = self.get_elements(self.__locators['消息项'])
            if not items:
                return
            identify_item = items[-1]
            pre = identify_item.location
            if desc_on:
                self.page_up()
            else:
                self.page_down()
            # 如果元素消失或者坐标发生变化，表示翻页后列表有新数据
            if ec.staleness_of(identify_item)(True) or not operator.eq(identify_item.location, pre):
                page_number += 1
                continue
            return
