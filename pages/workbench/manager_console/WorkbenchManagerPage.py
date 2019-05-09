from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class WorkBenchManagerPage(BasePage):
    """工作台管理首页"""

    ACTIVITY = ''

    __locators = {
        '返回': (MobileBy.ID, "com.chinasofti.rcs:id/btn_back_actionbar"),
        '应用': (MobileBy.XPATH, '//*[@text ="javascript:void(0);"]'),
        'X号': (MobileBy.ID, "com.chinasofti.rcs:id/btn_close_actionbar"),
        '加号': (MobileBy.XPATH, '//*[contains(@text,"javascript:addAppInBench")]'),
        '搜索应用': (MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.widget.EditText"),
        '搜索框': (MobileBy.XPATH, '//*[@class ="android.widget.EditText"]'),
        '搜索': (MobileBy.XPATH, '//*[@text ="搜索"]'),

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待工作台管理页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("公告信息")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在工作台管理页"""
        el = self.get_elements(self.__class__.__locators['应用'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["X号"])

    @TestLogger.log()
    def wait_for_store_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待应用商城页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present(
                    "javascript:toAppIntroduce('EIfNTEnWSwl1iDTPoGr4bQ==',1);")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_add(self):
        """点击加号"""
        self.click_element(self.__class__.__locators["加号"])

    @TestLogger.log()
    def input_store_name(self, name):
        """输入商店应用名称"""
        self.input_text(self.__class__.__locators["搜索框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_search(self):
        """点击搜索"""
        self.click_element(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def click_search_store(self):
        """点击搜索应用"""
        self.click_element(self.__class__.__locators["搜索应用"])
