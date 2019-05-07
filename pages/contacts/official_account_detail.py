from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components.menu_more import MenuMore


class OfficialAccountDetailPage(MenuMore, BasePage):
    """公众号详情"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountDetailActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '标题名称': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_title'),
        '公众号名称': (MobileBy.ID, 'com.chinasofti.rcs:id/public_name'),
        '更多菜单': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_more'),
        'com.chinasofti.rcs:id/public_scrollview_detail': (
            MobileBy.ID, 'com.chinasofti.rcs:id/public_scrollview_detail'),
        'com.chinasofti.rcs:id/public_header': (MobileBy.ID, 'com.chinasofti.rcs:id/public_header'),
        '公共账号：4011020490': (MobileBy.ID, 'com.chinasofti.rcs:id/public_account'),
        'com.chinasofti.rcs:id/public_introduction': (MobileBy.ID, 'com.chinasofti.rcs:id/public_introduction'),
        '功能介绍': (MobileBy.ID, 'com.chinasofti.rcs:id/intro_title'),
        '介绍整形美容知识，介绍美容整形情况！': (MobileBy.ID, 'com.chinasofti.rcs:id/intro_text'),
        'com.chinasofti.rcs:id/rl_public_auth': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_public_auth'),
        '认证主体': (MobileBy.ID, 'com.chinasofti.rcs:id/public_auth_text'),
        'com.chinasofti.rcs:id/public_auth_image': (MobileBy.ID, 'com.chinasofti.rcs:id/public_auth_image'),
        'com.chinasofti.rcs:id/ll_accept_message_push': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_accept_message_push'),
        '接收消息推送': (MobileBy.ID, ''),
        '开启': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_receive'),
        'com.chinasofti.rcs:id/ll_totop': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_totop'),
        '置顶公众号': (MobileBy.ID, ''),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_totop'),
        'com.chinasofti.rcs:id/ll_history_message': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_history_message'),
        '查看历史资讯': (MobileBy.ID, ''),
        'com.chinasofti.rcs:id/my_group_name_right_arrow': (
            MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name_right_arrow'),

        '进入公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_into_public'),
        '时间显示': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_time"]'),
        '历史资讯': (MobileBy.ID, 'com.chinasofti.rcs:id/pp_complex_1'),
    }

    # @TestLogger.log('点击返回')
    # def click_menu_more(self):
    #     self.click_element(self.__locators['返回'])

    @TestLogger.log('点击打开更多菜单')
    def click_menu_more(self):
        self.click_element(self.__locators['更多菜单'])

    @TestLogger.log()
    def page_contain_public_name(self,):
        """页面应该包含的元素-公众号名称"""
        return self.page_should_contain_element(self.__locators['公众号名称'])

    @TestLogger.log()
    def page_contain_public_title_name(self,):
        """页面应该包含的元素-公众号名称"""
        return self.page_should_contain_element(self.__locators['标题名称'])

    @TestLogger.log()
    def page_contain_public_header(self):
        """页面应该包含的元素-公众号头像"""
        return self.page_should_contain_element(self.__locators['com.chinasofti.rcs:id/public_header'])

    @TestLogger.log()
    def page_contain_public_number(self):
        """页面应该包含的元素-公共账号"""
        return self.page_should_contain_element(self.__locators['公共账号：4011020490'])

    @TestLogger.log()
    def page_contain_features(self):
        """页面应该包含的元素-功能介绍"""
        return self.page_should_contain_element(self.__locators['功能介绍'])

    @TestLogger.log()
    def page_contain_certification(self):
        """页面应该包含的元素-认证主体"""
        return self.page_should_contain_element(self.__locators['认证主体'])

    @TestLogger.log()
    def page_contain_read_more(self):
        """页面应该包含的元素-更多"""
        return self.page_should_contain_element(self.__locators['更多菜单'])

    @TestLogger.log('点击置顶公众号')
    def click_to_be_top(self):
        self.click_element(self.__locators['关闭'])

    @TestLogger.log('点击查看历史资讯')
    def click_read_old_message(self):
        self.click_element(self.__locators['com.chinasofti.rcs:id/my_group_name_right_arrow'])

    def swipe_page_up(self):
        """向上滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 50, 800)


    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待历史资讯页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["时间显示"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def page_contain_time(self):
        """页面应该包含的元素-时间"""
        try:
            pct=self.page_should_contain_element(self.__locators['时间显示'])
        except:
            self.swipe_page_up()
            pct=self.page_should_contain_element(self.__locators['时间显示'])
        return pct

    @TestLogger.log('点击进入公众号')
    def click_into_public(self):
        self.click_element(self.__locators['进入公众号'])

    @TestLogger.log('页面是否有历史资讯')
    def is_contain_old_mes(self):
        return self._is_element_present(self.__locators['历史资讯'])
