from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class HelpAndFeedBackPage(BasePage):
    """帮助与反馈页面"""
    __locators={
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '哪些人可以开通和使用和飞信': (MobileBy.XPATH, '//*[@text ="哪些人可以开通和使用和飞信？"]'),
        '如何登录及退出登录和飞信': (MobileBy.XPATH, '//*[@text ="如何登录及退出登录和飞信？"]'),
        '怎么开启和飞信同步手机通讯录的权限': (MobileBy.XPATH, '//*[@text ="怎么开启和飞信同步手机通讯录的权限？"]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self,timeout=3,auto_accept_alerts=True):
        """等待帮助与反馈页面加载（确保页面已经加载完成）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["如何登录及退出登录和飞信"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_question_one(self):
        """点击 哪些人可以开通和使用和飞信"""
        self.click_element(self.__class__.__locators["哪些人可以开通和使用和飞信"])

    @TestLogger.log()
    def click_question_two(self):
        """点击 如何登录及退出登录和飞信"""
        self.click_element(self.__class__.__locators["如何登录及退出登录和飞信"])

    @TestLogger.log()
    def clicl_question_three(self):
        """点击 怎么开启和飞信同步手机通讯录的权限"""
        self.click_element(self.__class__.__locators["怎么开启和飞信同步手机通讯录的权限"])

