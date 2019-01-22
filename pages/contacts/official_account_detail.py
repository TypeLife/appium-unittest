from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components.menu_more import MenuMore


class OfficialAccountDetailPage(MenuMore, BasePage):
    """公众号详情"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountDetailActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
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
        '进入公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_into_public')
    }

    @TestLogger.log('点击返回')
    def click_menu_more(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击打开更多菜单')
    def click_menu_more(self):
        self.click_element(self.__locators['更多菜单'])
