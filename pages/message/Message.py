from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class MessagePage(FooterPage):
    """主页 - 消息页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        "+号": (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/itemLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/itemLayout'),
        'com.chinasofti.rcs:id/pop_item_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_item_layout'),
        'com.chinasofti.rcs:id/iconIV': (MobileBy.ID, 'com.chinasofti.rcs:id/iconIV'),
        '新建消息': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="新建消息"]'),
        '免费短信': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="免费短信"]'),
        '发起群聊': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="发起群聊"]'),
        '分组群发': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="分组群发"]'),
        '扫一扫': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="扫一扫"]'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '页头-消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        'com.chinasofti.rcs:id/rv_conv_list': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_conv_list'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/search_edit'),
        '列表-消息块': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        '消息头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '消息名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        '消息简要内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe')
    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在消息页"""
        el = self.get_elements(self.__locators['+号'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_add_icon(self):
        """点击加号图标"""
        self.click_element(self.__locators['+号'])

    @TestLogger.log()
    def click_new_message(self):
        """点击新建消息"""
        self.click_element(self.__locators['新建消息'])

    @TestLogger.log()
    def assert_new_message_text_equal_to(self, expect):
        """检查新建消息菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['新建消息'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_free_sms(self):
        """点击免费短信"""
        self.click_element(self.__locators['免费短信'])

    @TestLogger.log()
    def assert_free_sms_text_equal_to(self, expect):
        """检查免费短信菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['免费短信'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_group_chat(self):
        """点击发起群聊"""
        self.click_element(self.__locators['发起群聊'])

    @TestLogger.log()
    def assert_group_chat_text_equal_to(self, expect):
        """检查发起群聊菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['发起群聊'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_group_mass(self):
        """点击分组群发"""
        self.click_element(self.__locators['分组群发'])

    @TestLogger.log()
    def assert_group_mass_text_equal_to(self, expect):
        """检查分组群发菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['分组群发'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_take_a_scan(self):
        """点击扫一扫"""
        self.click_element(self.__locators['扫一扫'])

    @TestLogger.log()
    def assert_take_a_scan_text_equal_to(self, expect):
        """检查扫一扫菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['扫一扫'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_search(self):
        """搜索"""
        self.click_element(self.__locators['搜索'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_login_success(self, timeout=8, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""

        def unexpect():
            result = self._is_element_present(
                [MobileBy.XPATH, '//*[@text="当前网络不可用(102101)，请检查网络设置"]'])
            return result

        try:
            self.wait_condition_and_listen_unexpected(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"]),
                unexpected=unexpect
            )
        except TimeoutException:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self
