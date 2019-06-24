import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components import LabelSettingMenu


class LableGroupDetailPage(LabelSettingMenu, BasePage):
    """标签分组详细页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.LabelContactListActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/rl_label_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_toolbar'),
        '返回': (MobileBy.XPATH, "//*[contains(@resource-id, 'back')]"),
        '标题': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_label_setting'),
        'com.chinasofti.rcs:id/recyclerView_contactList_label': (
            MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_contactList_label'),
        'com.chinasofti.rcs:id/contact_list': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
        'com.chinasofti.rcs:id/item_label_contact_head_item_id': (
            MobileBy.ID, 'com.chinasofti.rcs:id/item_label_contact_head_item_id'),
        'com.chinasofti.rcs:id/rl_first_cloum': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_first_cloum'),
        'com.chinasofti.rcs:id/layout_first_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_first_item'),
        'com.chinasofti.rcs:id/image_first_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
        '添加成员': (MobileBy.XPATH, '//*[@text="添加成员"]'),
        'com.chinasofti.rcs:id/layout_second_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_second_item'),
        'com.chinasofti.rcs:id/image_second_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_second_colum'),
        '群发信息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_second_colum'),
        'com.chinasofti.rcs:id/layout_third_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_third_item'),
        'com.chinasofti.rcs:id/image_third_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_third_colum'),
        'com.chinasofti.rcs:id/layout_fourth_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_fourth_item'),
        'com.chinasofti.rcs:id/image_fourth_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_fourth_colum'),
        '多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_fourth_colum'),

        '成员根节点': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        'A': (MobileBy.ID, ''),
        'com.chinasofti.rcs:id/name_head_rl': (MobileBy.ID, 'com.chinasofti.rcs:id/name_head_rl'),
        'com.chinasofti.rcs:id/content_ll': (MobileBy.ID, 'com.chinasofti.rcs:id/content_ll'),
        'axzq': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'azhl0001': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'B': (MobileBy.ID, ''),
        'bhl0002': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'D': (MobileBy.ID, ''),
        '大佬1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '大佬2': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '大佬3': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '成员名字': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'com.chinasofti.rcs:id/contact_index_bar_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
        'com.chinasofti.rcs:id/contact_index_bar_container': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
        'F': (MobileBy.ID, ''),
        '我知道了': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
    }

    @TestLogger.log("点击我知道了")
    def click_i_know(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['我知道了']):
            self.click_element(self.__class__.__locators['我知道了'])
        return True

    @TestLogger.log('获取分组名字')
    def get_group_name(self):
        name = self.get_text(self.__locators['标题'])
        return name

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('打开标签组设置菜单')
    def open_setting_menu(self):
        self.click_element(self.__locators['设置'])

    @TestLogger.log('点击群发信息')
    def click_send_group_info(self):
        """点击群发信息"""
        self.click_element(self.__locators['群发信息'])

    @TestLogger.log('点击添加成员')
    def click_add_members(self):
        """点击添加成员"""
        self.click_element(self.__locators['添加成员'])

    @TestLogger.log('点击多方通话')
    def click_multi_tel(self):
        """点击多方通话"""
        self.click_element(self.__locators['多方电话'])

    @TestLogger.log('点击多方视频')
    def click_multiparty_videos(self):
        """点击多方通话"""
        self.click_element(self.__locators['多方视频'])

    @TestLogger.log('检查点：当前页面为标签详情页')
    def assert_this_page_is_opened(self):
        try:
            self.wait_until(
                condition=lambda d: self.get_elements(self.__locators['添加成员'])
            )
        except TimeoutException:
            raise AssertionError('当前页面不是标签组详情页')

    @TestLogger.log("获取标签分组成员人名")
    def get_members_names(self):
        """获取标签分组成员人名"""
        els = self.get_elements(self.__class__.__locators['成员名字'])
        names = []
        if els:
            for el in els:
                names.append(el.text)
        return names

    @TestLogger.log('点击群发信息')
    def click_send_smsall(self):
        """点击群发信息"""
        self.click_element(self.__locators['com.chinasofti.rcs:id/image_second_colum'])
