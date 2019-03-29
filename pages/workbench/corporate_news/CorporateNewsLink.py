from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CorporateNewsLinkPage(BasePage):
    """发布新闻-链接发布页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '链接发布': (MobileBy.XPATH, '//*[@text="链接发布"]'),
        '图文发布': (MobileBy.XPATH, '//*[@text="图文发布"]'),
        '链接新闻': (MobileBy.XPATH, '//*[@text="链接新闻"]'),
        '新闻标题输入框': (MobileBy.XPATH, '//*[@resource-id="title_link"]'),
        '新闻网址输入框': (MobileBy.XPATH, '//*[@resource-id="linkUrl"]'),
        '保存': (MobileBy.XPATH, '//*[@text="保存"]'),
        '发布': (MobileBy.XPATH, '//*[@text="发布"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar')
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待发布新闻-链接发布页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["链接新闻"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def input_news_title(self, title):
        """输入链接新闻标题"""
        self.input_text(self.__class__.__locators["新闻标题输入框"], title)

    @TestLogger.log()
    def input_link_url(self, url):
        """输入链接新闻网址"""
        self.input_text(self.__class__.__locators["新闻网址输入框"], url)

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

    @TestLogger.log()
    def is_exist_save_successfully(self):
        """是否存在保存成功"""
        return self.is_toast_exist("保存成功")

    @TestLogger.log()
    def is_exist_release_successfully(self):
        """是否存在发布成功"""
        return self.is_toast_exist("发布成功")

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
