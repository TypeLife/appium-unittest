from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class LableGroupDetailPage(BasePage):
    """标签分组详细页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.LabelContactListActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/rl_label_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_toolbar'),
                  'com.chinasofti.rcs:id/rl_label_left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  'lab2': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
                  'com.chinasofti.rcs:id/iv_label_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_label_setting'),
                  'com.chinasofti.rcs:id/recyclerView_contactList_label': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_contactList_label'),
                  'com.chinasofti.rcs:id/contact_list': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
                  'com.chinasofti.rcs:id/item_label_contact_head_item_id': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/item_label_contact_head_item_id'),
                  'com.chinasofti.rcs:id/rl_first_cloum': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_first_cloum'),
                  'com.chinasofti.rcs:id/layout_first_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_first_item'),
                  'com.chinasofti.rcs:id/image_first_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                  '添加成员': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_first_colum'),
                  'com.chinasofti.rcs:id/layout_second_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_second_item'),
                  'com.chinasofti.rcs:id/image_second_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_second_colum'),
                  '群发信息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_second_colum'),
                  'com.chinasofti.rcs:id/layout_third_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_third_item'),
                  'com.chinasofti.rcs:id/image_third_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'),
                  '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_third_colum'),
                  'com.chinasofti.rcs:id/layout_fourth_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_fourth_item'),
                  'com.chinasofti.rcs:id/image_fourth_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_fourth_colum'),
                  '多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_fourth_colum'),
                  'com.chinasofti.rcs:id/rl_group_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
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
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  'F': (MobileBy.ID, ''),
                  }

    @TestLogger.log()
    def click_send_group_info(self):
        """点击群发信息"""
        self.click_element(self.__class__.__locators['群发信息'])

    @TestLogger.log()
    def click_add_members(self):
        """点击添加成员"""
        self.click_element(self.__class__.__locators['添加成员'])

    @TestLogger.log()
    def click_multi_tel(self):
        """点击多方通话"""
        self.click_element(self.__class__.__locators['多方电话'])
