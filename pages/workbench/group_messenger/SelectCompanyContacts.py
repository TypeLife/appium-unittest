from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectCompanyContactsPage(BasePage):
    """群发信使-》短信群发页面-》新建短信收件人选择页面"""
    ACTIVITY = ''

    __locators = {
        '新建短信': (MobileBy.XPATH, '//*[@text="新建短信"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        '搜索框': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '搜索框左边头像': (MobileBy.ID, 'com.chinasofti.rcs:id/avator'),
        '全选复选框': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_check_all'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("选择联系人")
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
        els = self.get_elements(self.__class__.__locators['返回'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 返回 控件")

    @TestLogger.log()
    def input_search_message(self, message):
        """输入查找信息"""
        self.input_text(self.__class__.__locators["搜索框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=10):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        els = self.get_elements(self.__class__.__locators['确定'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 确定 控件")

    @TestLogger.log()
    def is_left_head_exit(self):
        """搜索栏左侧被取消人员人名和头像是否存在"""
        if self._is_element_present(self.__class__.__locators['搜索框左边头像']):
            return True
        else:
            return False

    @TestLogger.log()
    def get_check_all(self):
        """获取全选复选框"""
        el = self.get_element(self.__class__.__locators['全选复选框'])
        return el