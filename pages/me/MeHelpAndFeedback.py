from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException


class MeHelpAndFeedbackPage(BasePage):
    """我-》帮助与反馈"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '帮助与反馈': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  '常见问题': (MobileBy.XPATH, "//*[contains(@text, '常见问题')]"),
                  '哪些人可以开通和使用和飞信': (MobileBy.XPATH, "//*[contains(@text, '哪些人可以开通和使用和飞信')]"),
                  '如何登录及退出登录和飞信': (MobileBy.XPATH, "//*[contains(@text, '如何登录及退出登录和飞信')]"),
                  "怎么开启和飞信同步手机通讯录的权限": (MobileBy.XPATH, "//*[contains(@text, '怎么开启和飞信同步手机通讯录的权限')]"),
                  '更多': (MobileBy.XPATH, "//*[contains(@text, '更多')]"),
                  '在线咨询': (MobileBy.XPATH, "//*[contains(@text, '在线咨询')]"),
                  '企业专家服务': (MobileBy.XPATH, "//*[contains(@text, '企业专家服务')]"),
                  '客服热线': (MobileBy.XPATH, "//*[contains(@text, '客服热线')]"),
                  '论坛互动': (MobileBy.XPATH, "//*[contains(@text, '论坛互动')]"),
                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '资费篇1': (MobileBy.XPATH, "//*[contains(@text, '资费篇')]"),
                  '每月10GB定向流量套餐是什么': (MobileBy.XPATH, "//*[contains(@text, '每月10GB定向流量套餐是什么')]"),
                  # 打开常见问题列表后元素
                  '常见问题标题': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),

                  '资费篇': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  }

    @TestLogger.log("""等待帮助与反馈页面加载""")
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["帮助与反馈"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("""点击H5按钮""")
    def click_text_button(self, locator, timeout=15):
        try:
            self.wait_until(
                condition=lambda d: self.get_element(self.__class__.__locators[locator])
            ).click()
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(timeout))

    @TestLogger.log("检查该页面包含文本")
    def page_contain_text(self, menu):
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log("检查该元素包含文本")
    def element_contain_text(self, locator, text):
        self.element_should_contain_text(self.__locators[locator], text)
