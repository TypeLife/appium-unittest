from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
import preconditions
class localContactPage(BasePage):
    """contacl_local"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
        MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        'com.chinasofti.rcs:id/action_add': (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/rv_conv_list': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_conv_list'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        '搜索2':(MobileBy.ID,'com.chinasofti.rcs:id/edit_query01'),
        'com.chinasofti.rcs:id/rl_conv_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_top': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_top'),
        '给个红包1': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '星期五': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        'com.chinasofti.rcs:id/ll_bottom': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_bottom'),
        '[名片]': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        'com.chinasofti.rcs:id/rl_conv_list_item656df904-3eee-43f2-a460-1bd24aad3596': (
        MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        'com.chinasofti.rcs:id/svd_head3191e8b6-7a2f-437b-bbb2-99e7c4d470c5': (
        MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_topcc8ef4f4-f913-4d63-8a05-623378be2cc1': (
        MobileBy.ID, 'com.chinasofti.rcs:id/ll_top'),
        '和飞信团队': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '星期五0c025608-c338-4a33-b2ad-7ec913a9496a': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        'com.chinasofti.rcs:id/ll_bottomf2fc45ad-d791-42a3-b29d-6eb9e6c88a40': (
        MobileBy.ID, 'com.chinasofti.rcs:id/ll_bottom'),
        'Hi，你好！欢迎使用和飞信！如‥': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        'com.chinasofti.rcs:id/ll_unread': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_unread'),
        'com.chinasofti.rcs:id/rnMessageBadge': (MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
        'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
        'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
        '消息2d55f4e2-9bbc-4537-ae5f-e07252b94d2f': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        'com.chinasofti.rcs:id/rnMessageBadge4a9f8e62-ef21-4a37-b28b-b31a82d4c6a4': (
        MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
        '联系人头像':(MobileBy.ID,'com.chinasofti.rcs:id/iv_head'),
        "联系人名字":(MobileBy.ID,'com.chinasofti.rcs:id/tv_name'),
        "联系人电话":(MobileBy.ID,'com.chinasofti.rcs:id/tv_phone')
    }

    @TestLogger.log("获取元素个数")
    def get_element_number(self,text="联系人头像"):
        return  self.get_elements(self.__locators[text])

    TestLogger.log("点击搜索框")
    def click_search_box(self):
        time.sleep(1)
        self.click_element(self.__locators['搜索'])

    TestLogger.log("输入搜索内容")
    def input_search_text(self,text='676560'):
        time.sleep(1)
        self.input_text(self.__locators['搜索2'],text)

    TestLogger.log("查看控件是否存在")
    def page_contain_element(self,text='联系人头像'):
        time.sleep(1)
        self.page_should_contain_element(self.__locators[text])

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """
        点击返回，通过android返回键
        """
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)