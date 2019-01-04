from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .dialogs import DeleteConfirmDialog


class LabelSettingMenu(DeleteConfirmDialog, BasePage):
    """标签设置"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.LabelGroupSettingActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_left_back'),
        '页面title': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_toolbar_title'),
        '标签名称': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_name'),
        '移除成员': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_remove_member'),
        '删除标签': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_delete_label'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击菜单：标签名称')
    def click_label_name_menu(self):
        self.click_element(self.__locators['标签名称'])

    @TestLogger.log('点击菜单：移除成员')
    def click_remove_member_menu(self):
        self.click_element(self.__locators['移除成员'])

    @TestLogger.log('点击菜单：删除标签')
    def click_delete_label_menu(self):
        self.click_element(self.__locators['删除标签'])
