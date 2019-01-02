from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class LabelGroupingPage(BasePage):
    """标签分组页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.group.GroupListActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/label_group_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/label_group_toolbar'),
                  'com.chinasofti.rcs:id/label_group_left_back': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/label_group_left_back'),
                  'com.chinasofti.rcs:id/toolbar_back_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_back_btn'),
                  '标签分组': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_toolbar_title'),
                  'com.chinasofti.rcs:id/group_list': (MobileBy.ID, 'com.chinasofti.rcs:id/group_list'),
                  'com.chinasofti.rcs:id/group_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/group_list_item'),
                  'com.chinasofti.rcs:id/asp_group_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/asp_group_icon'),
                  'com.chinasofti.rcs:id/group_name_linear_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name_linear_layout'),
                  '新建分组': (MobileBy.XPATH, '//*[@text="新建分组"]'),
                  'com.chinasofti.rcs:id/arrow_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_icon'),
                  'com.chinasofti.rcs:id/textView': (MobileBy.ID, 'com.chinasofti.rcs:id/textView'),
                  'lab2(11)': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
                  'mylab(5)': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
                  '标签分组名字': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
                  # 新建分组页面
                  '新建分组页面': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
                  '为你的分组创建一个名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sub_title'),
                  '请输入标签分组名称': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_group_name'),
                  }

    @TestLogger.log()
    def get_label_grouping_names(self):
        """获取标签分组名字"""
        els = self.get_elements(self.__class__.__locators["标签分组名字"])
        names = []
        for el in els:
            names.append(el.text)
        if "新建分组" in names:
            names.remove("新建分组")
        return names

    @TestLogger.log()
    def click_new_create_group(self):
        """点击新建分组"""
        self.click_element(self.__class__.__locators["新建分组"])

    @TestLogger.log()
    def select_group(self, name):
        """选择分组"""
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % name))

    @TestLogger.log()
    def input_label_grouping_name(self, name):
        """输入标签分组名称"""
        self.input_text(self.__class__.__locators["请输入标签分组名称"], name)

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待标签分组页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["标签分组"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def wait_for_create_label_grouping_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待新建标签分组页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新建分组页面"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self
