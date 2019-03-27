from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CorporateNewsImageTextPage(BasePage):
    """发布新闻-图文发布页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '图文发布': (MobileBy.XPATH, '//*[@text="图文发布"]'),
        '链接发布': (MobileBy.XPATH, '//*[@text="链接发布"]'),
        '新闻内容': (MobileBy.XPATH, '//*[@text="新闻内容"]'),
        '新闻标题输入框': (MobileBy.XPATH, '//*[@resource-id="title"]'),
        '新闻内容输入框': (MobileBy.XPATH, '//*[@resource-id="content"]'),
        '保存': (MobileBy.XPATH, '//*[@text="保存"]'),
        '发布': (MobileBy.XPATH, '//*[@text="发布"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]')
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待发布新闻-图文发布页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新闻内容"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def input_news_title(self, title):
        """输入图文新闻标题"""
        self.input_text(self.__class__.__locators["新闻标题输入框"], title)

    @TestLogger.log()
    def input_news_content(self, content):
        """输入图文新闻内容"""
        self.input_text(self.__class__.__locators["新闻内容输入框"], content)

    @TestLogger.log()
    def click_link_publishing(self):
        """点击链接发布"""
        self.click_element(self.__class__.__locators["链接发布"])

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_release(self):
        """点击发布"""
        self.click_element(self.__class__.__locators["发布"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])
