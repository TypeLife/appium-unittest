from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SetMessageNoticePage(BasePage):
    """我-》设置-》消息通知"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingActivity'

    __locators = {
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '菜单列表框': (MobileBy.XPATH, '//android.widget.ScrollView/android.widget.LinearLayout'),
        '消息通知': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '接收新消息通知': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_isOpen'),
        '去设置': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_app_notification_tip'),
        '通知栏显示消息详情': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_available'),
        '消息送达状态显示': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_receipt'),
        '声音提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_sound'),
        '震动提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_shake'),
        '接收OA消息': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_oa'),
        '接收139邮箱助手消息': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_139'),
    }

    @TestLogger.log("打开设置项")
    def turn_on(self, item):
        """
        Example: self.turn_on("声音提醒")
        :param item: 设置项在界面上的名称
        :return:
        """
        switch_locator = [
            MobileBy.XPATH,
            '//android.widget.Switch[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(switch_locator)

        open_states = ['开启']
        close_states = ['关闭']
        current_status = self.get_text(switch_locator)
        if current_status in open_states:
            return
        elif current_status in close_states:
            self.click_element(switch_locator)
            assert self.get_text(switch_locator) in open_states
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

        open_states = ['开启']
        close_states = ['关闭']
        current_status = self.get_text(switch_locator)
        if current_status in open_states:
            self.click_element(switch_locator)
            assert self.get_text(switch_locator) in close_states
        elif current_status in close_states:
            return
        else:
            raise Exception("{} not in {} and {}".format(current_status, open_states, close_states))

    @TestLogger.log("检查设置项是否打开")
    def assert_menu_item_has_been_turn_on(self, item):
        switch_locator = [
            MobileBy.XPATH,
            '//android.widget.Switch[../android.widget.TextView[@text="{}"]]'.format(item)
        ]

        self._find_item(switch_locator)

        open_states = ['开启']
        close_states = ['关闭']
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

        open_states = ['开启']
        close_states = ['关闭']
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
        return self._is_element_present(self.__locators['接收新消息通知'])

    def _is_on_the_end_of_menu_view(self):
        """判断是否在菜单末尾"""
        return self._is_element_present(self.__locators['接收139邮箱助手消息'])
