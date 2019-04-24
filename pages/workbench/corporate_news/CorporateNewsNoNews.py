import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage


class CorporateNewsNoNewsPage(BasePage):
    """未发新闻页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '未发新闻': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_actionbar"),
        '新闻名称': (MobileBy.XPATH, '//*[@resource-id="news_title"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar')
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待未发新闻页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["未发新闻"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_exist_no_news(self):
        """是否存在未发新闻"""
        els = self.get_elements(self.__class__.__locators["新闻名称"])
        return len(els) > 0

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_no_news_by_number(self, number):
        """点击某一条未发新闻,返回标题"""
        if self._is_element_present(self.__class__.__locators["新闻名称"]):
            els = self.get_elements(self.__class__.__locators["新闻名称"])
            title = els[number].text
            els[number].click()
            return title

    @TestLogger.log()
    def is_exist_no_news_by_name(self, name):
        """是否存在指定未发新闻"""
        els = self.get_elements((MobileBy.XPATH, '//*[@resource-id="news_title" and @text="%s"]' % name))
        return len(els) > 0

    @TestLogger.log()
    def clear_no_news(self):
        """清空未发新闻"""
        current = 0
        while self._is_element_present(self.__class__.__locators["新闻名称"]):
            current += 1
            if current > 5:
                return
            els = self.get_elements(self.__class__.__locators["新闻名称"])
            cndp = CorporateNewsDetailsPage()
            for el in els:
                el.click()
                cndp.wait_for_page_load()
                cndp.click_delete()
                cndp.click_sure()
                time.sleep(2)
                self.wait_for_page_load()
