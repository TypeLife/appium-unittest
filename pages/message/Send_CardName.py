from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components import BaseChatPage


class Send_CardNamePage(BaseChatPage):
    """个人名片"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UserProfileShowActivity'

    __locators = {
        '关闭X': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_img'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_img'),
        '姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
        '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
        '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/company_tv'),
        '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/position_tv'),
        '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/email_tv'),
        '发送名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv')
    }

    @TestLogger.log('关闭')
    def click_close_btn(self):
        self.click_element(self.__locators['关闭X'])

    @TestLogger.log('发送名片')
    def click_share_btn(self):
        self.click_element(self.__locators['发送名片'])

    @TestLogger.log()
    def assert_card_name_equal_to(self, expect):
        """检查姓名"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['姓名'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def is_present_card_phone(self, timeout=3, auto_accept_alerts=True):
        """是否出现头像"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["头像"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def assert_card_phone_equal_to(self, expect):
        """检查电话"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['电话'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def assert_card_comp_equal_to(self, expect):
        """检查公司"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['公司'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def assert_card_position_equal_to(self, expect):
        """检查职位"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['职位'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def assert_card_emailaddress_equal_to(self, expect):
        """检查邮箱"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['邮箱'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))
