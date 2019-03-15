from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SmsSettingPage(BasePage):
    """ 我-》设置-》短信设置"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SmsSettingActivity'

    __locators = {
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '短信设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '菜单列表框': (MobileBy.XPATH, '//android.widget.ScrollView/android.widget.LinearLayout'),
        '应用内收发短信': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_sms'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_sms'),
        '弹框提示内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
    }

    @TestLogger.log('点击返回上一页图标')
    def click_back(self):
        self.click_element(self.__locators['返回上一页'])

    @TestLogger.log('点击按钮')
    def click_button(self, name):
        locator = [MobileBy.XPATH, '//android.widget.Button[@text="{}"]'.format(name)]
        self.click_element(locator, 1)

    @TestLogger.log("打开设置项")
    def turn_on(self, item):
        """
        Example: self.turn_on("应用内收发短信")
        :param item: 设置项在界面上的名称
        :return:
        """
        switch_locator = [
            MobileBy.XPATH,
            '//android.widget.Switch[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(switch_locator)

        open_states = ['开启', '打开', 'ON']
        close_states = ['关闭', 'OFF']
        current_status = self.get_text(switch_locator)
        if current_status in open_states:
            return
        elif current_status in close_states:
            self.click_element(switch_locator)
        else:
            raise Exception("{} not in {} and {}".format(current_status, open_states, close_states))

    @TestLogger.log("关闭设置项")
    def turn_off(self, item):
        """
        Example: self.turn_off("声音提醒")
        :param item: 设置项在界面上的名称
        :return:
        """
        switch_locator = [
            MobileBy.XPATH,
            '//android.widget.Switch[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(switch_locator)

        open_states = ['开启', '打开', 'ON']
        close_states = ['关闭', 'OFF']
        current_status = self.get_text(switch_locator)
        if current_status in open_states:
            self.click_element(switch_locator)
            assert self.get_text(switch_locator) in close_states
        elif current_status in close_states:
            return
        else:
            raise Exception("{} not in {} and {}".format(current_status, open_states, close_states))

    @TestLogger.log("勾选复选框")
    def check_checkbox(self, item):
        """
        Example: self.check_checkbox("展示最近一个月内的短信记录")
        :param item: 界面上的设置项名称
        :return:
        """
        locator = [
            MobileBy.XPATH,
            '//android.widget.CheckBox[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(locator)
        status_attr = 'checked'
        checked_states = ['true']
        unchecked_states = ['false']
        current_status = self.get_element_attribute(locator, status_attr, 1)
        if current_status in checked_states:
            return
        elif current_status in unchecked_states:
            self.click_element(locator)
        else:
            raise Exception("{} not in {} and {}".format(current_status, checked_states, unchecked_states))

    @TestLogger.log("去勾选复选框")
    def uncheck_checkbox(self, item):
        """
        Example: self.uncheck_checkbox("展示最近一个月内的短信记录")
        :param item: 界面上的设置项在名称
        :return:
        """
        locator = [
            MobileBy.XPATH,
            '//android.widget.CheckBox[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(locator)
        status_attr = 'checked'
        checked_states = ['true']
        unchecked_states = ['false']
        current_status = self.get_element_attribute(locator, status_attr, 1)
        if current_status in checked_states:
            self.click_element(locator)
        elif current_status in unchecked_states:
            return
        else:
            raise Exception("{} not in {} and {}".format(current_status, checked_states, unchecked_states))

    @TestLogger.log("检查设置项是否打开")
    def assert_menu_item_has_been_turn_on(self, item):
        switch_locator = [
            MobileBy.XPATH,
            '//android.widget.Switch[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(switch_locator)

        open_states = ['开启', '打开', 'ON']
        close_states = ['关闭', 'OFF']
        current_status = self.get_text(switch_locator)
        if current_status in open_states:
            return
        elif current_status in close_states:
            raise AssertionError('设置项"{}"没有打开，当前状态为：{}'.format(item, current_status))
        else:
            raise Exception("{} not in {} and {}".format(current_status, open_states, close_states))

    @TestLogger.log("检查设置项是否关闭")
    def assert_menu_item_has_been_turn_off(self, item):
        switch_locator = [
            MobileBy.XPATH,
            '//android.widget.Switch[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(switch_locator)

        open_states = ['开启', '打开', 'ON']
        close_states = ['关闭', 'OFF']
        current_status = self.get_text(switch_locator)
        if current_status in open_states:
            raise AssertionError('设置项"{}"没有关闭，当前状态为：{}'.format(item, current_status))
        elif current_status in close_states:
            return
        else:
            raise Exception("{} not in {} and {}".format(current_status, open_states, close_states))

    @TestLogger.log("下一页")
    def page_down(self):
        """下一页"""
        self.swipe_by_direction(self.__locators['菜单列表框'], 'up')

    @TestLogger.log("上一页")
    def page_up(self):
        """上一页"""
        self.swipe_by_direction(self.__locators['菜单列表框'], 'down')

    @TestLogger.log("滚动列表到顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单列表框'])
        )
        if self._is_on_the_start_of_menu_view():
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_on_the_start_of_menu_view():
                break
        return True

    @TestLogger.log("滚动到列表底部")
    def scroll_to_bottom(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单列表框'])
        )
        if self._is_on_the_end_of_menu_view():
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_down()
            if self._is_on_the_end_of_menu_view():
                break
        return True

    def _find_item(self, locator):
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            max_try = 5
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if self._is_on_the_end_of_menu_view():
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    def _is_on_the_start_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['应用内收发短信'])

    def _is_on_the_end_of_menu_view(self):
        """判断是否在菜单末尾"""
        return self._is_element_present(self.__locators['应用内收发短信'])
