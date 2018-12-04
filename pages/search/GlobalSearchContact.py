from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class GlobalSearchContactPage(Keyboard, BasePage):
    """查看更多联系人"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.GlobalSearchContactActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '输入关键字搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
        '清空关键字': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '数据类型名称': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '列表': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/result_list"]/*'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
        '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])
