from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.Footer import FooterPage


class MePage(FooterPage):
    """ 我 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/titleBar': (MobileBy.ID, 'com.chinasofti.rcs:id/titleBar'),
        '页头-我': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '页脚-我': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvMe" and @selected="true"]'),
        '二维码入口': (MobileBy.ID, 'com.chinasofti.rcs:id/qr_code_imageview'),
        'com.chinasofti.rcs:id/rl_person': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_person'),
        'com.chinasofti.rcs:id/fl_name': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_name'),
        '请完善名片': (MobileBy.ID, 'com.chinasofti.rcs:id/card_name_hint'),
        '14775970982': (MobileBy.ID, 'com.chinasofti.rcs:id/card_photo_num'),
        '查看并编辑个人资料': (MobileBy.ID, 'com.chinasofti.rcs:id/check_user_profile'),
        'com.chinasofti.rcs:id/profile_photo_out': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo_out'),
        'com.chinasofti.rcs:id/avatar_bg_id': (MobileBy.ID, 'com.chinasofti.rcs:id/avatar_bg_id'),
        'com.chinasofti.rcs:id/card_head_photo': (MobileBy.ID, 'com.chinasofti.rcs:id/card_head_photo'),
        'com.chinasofti.rcs:id/layout_for_mall': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_mall'),
        'com.chinasofti.rcs:id/internet_mutil_call_layout_id': (
            MobileBy.ID, 'com.chinasofti.rcs:id/internet_mutil_call_layout_id'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_name_text'),
        '300': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_number_text'),
        '分钟': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_unit'),
        'com.chinasofti.rcs:id/user_money': (MobileBy.ID, 'com.chinasofti.rcs:id/user_money'),
        '账户余额': (MobileBy.ID, 'com.chinasofti.rcs:id/money_name_text'),
        '12.20': (MobileBy.ID, 'com.chinasofti.rcs:id/money_number_text'),
        '元': (MobileBy.ID, 'com.chinasofti.rcs:id/money_unit'),
        'com.chinasofti.rcs:id/layout_flow': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_flow'),
        '可用流量': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_name_text'),
        '40.98': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_number_text'),
        'G': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_unit'),
        'com.chinasofti.rcs:id/redpager': (MobileBy.ID, 'com.chinasofti.rcs:id/redpager'),
        '钱包': (MobileBy.ID, 'com.chinasofti.rcs:id/repager_text'),
        'com.chinasofti.rcs:id/welfare': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare'),
        '福利': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare_text'),
        '多重好礼等你来领': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
        'com.chinasofti.rcs:id/wfSpace': (MobileBy.ID, 'com.chinasofti.rcs:id/wfSpace'),
        'com.chinasofti.rcs:id/welfareArrow': (MobileBy.ID, 'com.chinasofti.rcs:id/welfareArrow'),
        'com.chinasofti.rcs:id/collect': (MobileBy.ID, 'com.chinasofti.rcs:id/collect'),
        '收藏': (MobileBy.ID, 'com.chinasofti.rcs:id/collect_text'),
        'com.chinasofti.rcs:id/about_app': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app'),
        '关于和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app_text'),
        'com.chinasofti.rcs:id/about_right_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/about_right_arrow'),
        'com.chinasofti.rcs:id/share_app': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app'),
        'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
        'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        'com.chinasofti.rcs:id/rnMessageBadge': (MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
        'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground'),
        '推荐好友，赚现金红包': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
        '分享客户端': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app_text'),
        'com.chinasofti.rcs:id/feedback': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback'),
        '帮助与反馈': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback_text'),
        'com.chinasofti.rcs:id/setting': (MobileBy.ID, 'com.chinasofti.rcs:id/setting'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_app_text'),

    }

    @TestLogger.log()
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['我'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')

    @TestLogger.log()
    def click_setting_menu(self):
        """点击设置菜单"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['设置'])
        ).click()
        # self.click_element(self.__locators['设置'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """判断页面是否包含选中状态的“我”页脚标签"""
        try:
            self.wait_until(
                condition=lambda d: self.get_element(self.__locators['页脚-我']),
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self
