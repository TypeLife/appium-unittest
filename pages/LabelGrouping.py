from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components import ContactsSelector


class LabelGroupingPage(ContactsSelector, BasePage):
    """标签分组页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.group.GroupListActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/label_group_toolbar': (
            MobileBy.ID, 'com.chinasofti.rcs:id/label_group_toolbar'),
        '返回': (MobileBy.XPATH, '//*[contains(@resource-id,"back")]'),
        '标签分组': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_toolbar_title'),
        'com.chinasofti.rcs:id/group_list': (MobileBy.ID, 'com.chinasofti.rcs:id/group_list'),
        '分组根节点': (MobileBy.ID, 'com.chinasofti.rcs:id/group_list_item'),
        '分组图标': (MobileBy.ID, 'com.chinasofti.rcs:id/asp_group_icon'),
        '新建分组': (MobileBy.XPATH, '//*[@text="新建分组"]'),
        '分组右侧箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_icon'),
        'com.chinasofti.rcs:id/textView': (MobileBy.ID, 'com.chinasofti.rcs:id/textView'),
        'biao': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
        'mylab(5)': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
        '标签分组名字': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
        # 新建分组页面
        '新建分组页面': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '为你的分组创建一个名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sub_title'),
        '请输入标签分组名称': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_group_name'),
    }

    @TestLogger.log('删除全部标签')
    def delete_all_label(self):
        from pages import LableGroupDetailPage
        groups = self.get_elements(self.__locators['分组根节点'])[1:]
        while groups:
            groups[0].click()
            # 删除标签
            detail = LableGroupDetailPage()
            try:
                self.click_element(['xpath', '//*[@text="我知道了"]'], 1)
            except:
                pass
            detail.open_setting_menu()
            detail.click_delete_label_menu()
            detail.click_delete()
            self.wait_for_page_load()
            # 刷新group
            groups = self.get_elements(self.__locators['分组根节点'])[1:]

    @TestLogger.log('检查默认文案')
    def assert_default_status_is_right(self):
        self.mobile.assert_screen_contain_text('暂无分组')

    @TestLogger.log('获取标签分组名字')
    def get_label_grouping_names(self):
        """获取标签分组名字"""
        els = self.get_elements(self.__class__.__locators["标签分组名字"])
        names = []
        for el in els:
            names.append(el.text)
        if "新建分组" in names:
            names.remove("新建分组")
        return names

    @TestLogger.log('点击新建分组')
    def click_new_create_group(self):
        """点击新建分组"""
        self.click_element(self.__class__.__locators["新建分组"])

    @TestLogger.log('选择分组')
    def select_group(self, name):
        """选择分组"""
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % name))

    @TestLogger.log('输入标签分组名称')
    def input_label_grouping_name(self, name):
        """输入标签分组名称"""
        self.input_text(self.__class__.__locators["请输入标签分组名称"], name)

    @TestLogger.log('点击确定')
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log('等待标签分组页面加载')
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

    @TestLogger.log('等待新建标签分组页面加载')
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

    @TestLogger.log('创建分组')
    def create_group(self, group_name, *member_list):
        self.click_new_create_group()
        self.wait_for_create_label_grouping_page_load()
        self.input_label_grouping_name(group_name)
        self.click_sure()
        if self.is_group_exist_tips_popup():
            print('群组："{}" 已存在'.format(group_name))
            self.click_back()
            return
        if not member_list:
            self.click_back()
            self.click_back()
            return
        self.select_local_contacts(*member_list)

    @TestLogger.log('判断点击确定后“群组已存在”提示是否弹出')
    def is_group_exist_tips_popup(self):
        try:
            self.wait_condition_and_listen_unexpected(
                condition=lambda d: self.is_text_present('选择和通讯录联系人'),
                unexpected=lambda: self.get_elements(['xpath', '//*[@text="群组已存在"]']),
            )
            return False
        except AssertionError:
            return True

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])
