import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ImportantMattersPage(BasePage):
    """重要事项首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '新建事项': (MobileBy.XPATH, '//*[@text="新建事项"]'),
        '创建事项': (MobileBy.XPATH, '//*[@text="创建事项"]'),
        '归档事项': (MobileBy.XPATH, '//*[@text="归档事项"]'),
        '删除事项': (MobileBy.XPATH, '//*[@text="删除事项"]'),
        '进行中的事项标题': (MobileBy.XPATH, '//*[contains(@text,"创建")]/../../../android.view.View[1]/android.view.View'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '保存': (MobileBy.XPATH, '//*[@text="保存"]'),
        '人员状态': (MobileBy.XPATH, '//*[@text="人员状态"]'),
        '添加人员': (MobileBy.XPATH, '//*[@text="添加人员"]'),
        '删除人员': (MobileBy.XPATH, '//*[@text="删除人员"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '创建事项页面标题输入框': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.widget.EditText'),
        '查看事项页面标题输入框': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[2]'),
        '创建事项页面描述输入框': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.EditText'),
        '查看事项页面描述输入框': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]'),
        '事项修改编辑框': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.widget.EditText'),
        '+号': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[4]/android.widget.ListView/android.view.View[2]/android.view.View[1]/android.view.View'),
        '事项标题栏三点': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View[1]/android.view.View[3]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待重要事项首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新建事项"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_important_matters_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在重要事项首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新建事项"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_new_item(self):
        """点击新建事项"""
        self.click_element(self.__class__.__locators["新建事项"])

    @TestLogger.log()
    def click_create_item(self):
        """点击创建事项"""
        self.click_element(self.__class__.__locators["创建事项"])

    @TestLogger.log()
    def wait_for_create_item_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待创建事项页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["创建事项"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_check_item_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待查看事项页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["归档事项"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_personnel_status_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待人员状态页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["添加人员"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def input_create_item_title(self, title):
        """输入创建事项页面标题"""
        self.input_text(self.__class__.__locators["创建事项页面标题输入框"], title)

    @TestLogger.log()
    def input_create_item_describe(self, describe):
        """输入创建事项页面描述"""
        self.input_text(self.__class__.__locators["创建事项页面描述输入框"], describe)

    @TestLogger.log()
    def input_modify_content(self, content):
        """输入修改内容"""
        self.input_text(self.__class__.__locators["事项修改编辑框"], content)

    @TestLogger.log()
    def click_check_item_title(self):
        """点击查看事项页面标题"""
        self.click_element(self.__class__.__locators["查看事项页面标题输入框"])

    @TestLogger.log()
    def click_check_item_describe(self):
        """点击查看事项页面描述"""
        self.click_element(self.__class__.__locators["查看事项页面描述输入框"])

    @TestLogger.log()
    def click_add_icon(self):
        """点击+号"""
        self.click_element(self.__class__.__locators["+号"])

    @TestLogger.log()
    def click_three_points_icon(self):
        """点击事项标题栏右侧三点"""
        self.click_element(self.__class__.__locators["事项标题栏三点"])

    @TestLogger.log()
    def click_delete_item(self):
        """点击删除事项"""
        self.click_element(self.__class__.__locators["删除事项"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_personnel_status(self):
        """点击人员状态"""
        self.click_element(self.__class__.__locators["人员状态"])

    @TestLogger.log()
    def click_add_personnel(self):
        """点击添加人员"""
        self.click_element(self.__class__.__locators["添加人员"])

    @TestLogger.log()
    def click_delete_personnel(self):
        """点击删除人员"""
        self.click_element(self.__class__.__locators["删除人员"])

    @TestLogger.log()
    def click_first_item(self):
        """点击第一条进行中的事项"""
        els = self.get_elements(self.__class__.__locators["进行中的事项标题"])
        els[0].click()

    @TestLogger.log()
    def is_exists_item(self):
        """是否存在已有事项"""
        return self._is_element_present(self.__class__.__locators["进行中的事项标题"])

    @TestLogger.log()
    def is_exists_delete_icon_by_name(self, name):
        """是否存在指定联系人删除图标"""
        locator = (MobileBy.XPATH, '//*[@text="%s"]/../android.view.View[2]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def click_delete_icon_by_name(self, name):
        """点击指定联系人删除图标"""
        locator = (MobileBy.XPATH, '//*[@text="%s"]/../android.view.View[2]' % name)
        self.click_element(locator)

    @TestLogger.log()
    def clear_item(self):
        """清空进行中的事项"""
        current = 0
        while self._is_element_present(self.__class__.__locators["进行中的事项标题"]):
            current += 1
            if current > 5:
                return
            els = self.get_elements(self.__class__.__locators["进行中的事项标题"])
            for el in els:
                el.click()
                self.wait_for_check_item_page_load()
                self.click_three_points_icon()
                time.sleep(2)
                self.click_delete_item()
                time.sleep(1)
                self.click_sure()
                self.wait_for_page_load()
