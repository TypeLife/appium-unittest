import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage


class CorporateNewsPage(BasePage):
    """企业新闻首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '企业新闻': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_actionbar"),
        '发布新闻': (MobileBy.XPATH, '//*[@resource-id="publishNews" and @text="发布新闻"]'),
        '未发新闻': (MobileBy.XPATH, '//*[@resource-id="toPublish" and @text="未发新闻"]'),
        '新闻名称': (MobileBy.XPATH, '//*[@resource-id="news_title"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '提示语': (MobileBy.XPATH, "//*[contains(@text, '向团队所有成员发出第一条新闻')]"),
        '右上角搜索图标': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        '搜索框': (MobileBy.XPATH, '//*[@resource-id="cNewsTitle"]'),
        '搜索': (MobileBy.XPATH, '//*[@text="搜索"]'),
        '浏览量': (MobileBy.XPATH, '//*[@resource-id="news_traffic"]')
    }

    @TestLogger.log()
    def is_on_corporate_news_page(self, timeout=60, auto_accept_alerts=True):
        """当前页面是否在企业新闻首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发布新闻"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待企业新闻首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发布新闻"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_release_news(self):
        """点击发布新闻"""
        self.click_element(self.__class__.__locators["发布新闻"])

    @TestLogger.log()
    def click_no_news(self):
        """点击未发新闻"""
        self.click_element(self.__class__.__locators["未发新闻"])

    @TestLogger.log()
    def is_exist_corporate_news(self):
        """是否存在企业新闻"""
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
    def clear_corporate_news(self):
        """清空企业新闻"""
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
                cndp.click_offline()
                cndp.click_sure()
                time.sleep(2)
                self.wait_for_page_load()

    @TestLogger.log()
    def is_exist_words(self):
        """是否存在提示语"""
        return self._is_element_present(self.__class__.__locators["提示语"])

    @TestLogger.log()
    def is_exist_release_news_button(self):
        """是否存在发布新闻按钮"""
        return self._is_element_present(self.__class__.__locators["发布新闻"])

    @TestLogger.log()
    def is_exist_no_news_button(self):
        """是否存在未发新闻按钮"""
        return self._is_element_present(self.__class__.__locators["未发新闻"])

    @TestLogger.log()
    def get_corporate_news_titles(self):
        """获取企业新闻标题"""
        if self._is_element_present(self.__class__.__locators["新闻名称"]):
            els = self.get_elements(self.__class__.__locators["新闻名称"])
            titles = []
            for el in els:
                title = el.text
                titles.insert(0, title)
            return titles

    @TestLogger.log()
    def is_exist_close_button(self):
        """是否存在关闭按钮"""
        return self._is_element_present(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_search_icon(self):
        """点击右上角搜索图标"""
        self.click_element(self.__class__.__locators["右上角搜索图标"])

    @TestLogger.log()
    def input_search_content(self, content):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators["搜索框"], content)

    @TestLogger.log()
    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def get_current_corporate_news_number(self):
        """获取当前企业新闻数"""
        els = self.get_elements(self.__class__.__locators["新闻名称"])
        return len(els)

    @TestLogger.log()
    def click_corporate_news_by_number(self, number):
        """点击某一条企业新闻"""
        if self._is_element_present(self.__class__.__locators["浏览量"]):
            els = self.get_elements(self.__class__.__locators["浏览量"])
            els[number].click()

    @TestLogger.log()
    def get_corporate_news_page_view_by_number(self, number):
        """返回某一条企业新闻浏览量"""
        if self._is_element_present(self.__class__.__locators["浏览量"]):
            els = self.get_elements(self.__class__.__locators["浏览量"])
            amount = els[number].text
            return int(amount)
