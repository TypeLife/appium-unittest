import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException


class MeCallMultiPage(BasePage):
    """我-》多方通话"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.MultiCallRechargeManageActivity'

    __locators = {'': (MobileBy.ID, ''),

                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '	多方电话管理': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
                  'Q&A': (MobileBy.ID, 'com.chinasofti.rcs:id/img_multi_time'),
                  '充值中心': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_recharge'),
                  '资费说明': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_instruction'),
                  '当前剩余多方通话分钟数': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_recharge_name'),
                  '100': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_remainder_duration'),
                  '分钟': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_min'),
                  # 打开当前剩余多方电话分钟
                  '充值': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_recharge_button'),
                  # 打开充值中心页面
                  '查看充值记录': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_recharge_record'),
                  '充值套餐': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_recharge_package'),
                  '返回1': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  # 6.3.1版本飞信电话可用时长
                  '分钟_631': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_unit'),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待卡片页面弹框加载 """
        try:
            time.sleep(5)
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["100"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("检查该页面包含多个文本")
    def page_contain_text(self, menu):
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log()
    def click_el_text(self, locator):
        """点击字段选项 """
        self.click_element(self.__locators[locator])

    @TestLogger.log()
    def page_contain_ele(self, locator):
        """该页面是否包含字段 """
        self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log()
    def wait_for_page_load_call_questions(self, timeout=20, auto_accept_alerts=True):
        """等待多方电话FQA页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("当前剩余通话时长：")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_call_details(self, timeout=20, auto_accept_alerts=True):
        """等待多方电话时长详情页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("和飞信基本套餐")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_call_details_charge(self, text, timeout=20, auto_accept_alerts=True,):
        """等待多方电话时长详情页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present(text)
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_charge_center(self, timeout=8, auto_accept_alerts=True):
        """等待多方电话时长详情页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("充值套餐")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def ele_is_click(self, locator):
        """点击字段选项 """
        self.element_should_be_enabled(self.__locators[locator])

    @TestLogger.log()
    def is_mutil_call_manage(self):
        """当前是否在多方电话管理页面"""
        self.element_should_contain_text((MobileBy.ID, "com.chinasofti.rcs:id/label_toolbar_title"), '多方电话管理')

    @TestLogger.log()
    def is_mutil_call_manage_631(self):
        """当前是否在飞信电话管理页面 6.3.1版本"""
        flag = False
        element = self.get_elements(self.__locators["多方电话管理"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_mutilcall_manage(self):
        """点击多方电话可用时长"""
        self.click_element(self.__locators['分钟'])

    @TestLogger.log()
    def click_mutilcall_manage_631(self):
        """点击多方电话可用时长 6.3.1版本"""
        self.click_element(self.__locators['分钟_631'])




