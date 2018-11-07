from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.Footer import FooterPage


class MessagePage(FooterPage):
    """消息页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        "+号": (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/itemLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/itemLayout'),
        'com.chinasofti.rcs:id/pop_item_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_item_layout'),
        'com.chinasofti.rcs:id/iconIV': (MobileBy.ID, 'com.chinasofti.rcs:id/iconIV'),
        '新建消息': (
            MobileBy.XPATH, '//*[@text ="新建消息"]'),
        '免费短信': (
            MobileBy.XPATH, '//*[@text ="免费短信"]'),
        '发起群聊': (
            MobileBy.XPATH, '//*[@text ="发起群聊"]'),
        '分组群发': (
            MobileBy.XPATH, '//*[@text ="分组群发"]'),
        '扫一扫': (
            MobileBy.XPATH, '//*[@resource_id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="扫一扫"]'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        'com.chinasofti.rcs:id/action_add': (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/rv_conv_list': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_conv_list'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/search_edit'),
        'com.chinasofti.rcs:id/rl_conv_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_top': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_top'),
        '和飞信团队': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '11:00': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        'com.chinasofti.rcs:id/ll_bottom': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_bottom'),
        'Hi，你好！欢迎使用和飞信！如果需要…': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
        'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe')
    }

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
