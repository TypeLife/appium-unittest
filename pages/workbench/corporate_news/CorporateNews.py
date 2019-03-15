from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CorporateNewsPage(BasePage):
    """企业新闻页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '企业新闻': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '发布新闻': (MobileBy.XPATH, '//*[@resource-id="publishNews"]'),
        '未发新闻': (MobileBy.XPATH, '//*[@resource-id="toPublish"]'),
        '链接发布': (MobileBy.XPATH, '//*[@text="链接发布"]'),
        '新闻标题': (MobileBy.XPATH, '//*[@resource-id="title_link"]'),
        '链接新闻': (MobileBy.XPATH, '//*[@resource-id="linkUrl"]'),
        '保存': (MobileBy.XPATH, '//*[@text="保存"]'),
        '发布': (MobileBy.XPATH, '//*[@text="发布"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
        '新闻标题选择框': (MobileBy.XPATH, '//*[@resource-id="news_title"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '删除': (MobileBy.XPATH, '//*[@text="删除"]')
    }

    @TestLogger.log()
    def is_on_corporate_news_page(self):
        """当前页面是否在企业新闻首页"""

        try:
            self.wait_until(
                timeout=10,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["企业新闻"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_release_news(self):
        """点击发布新闻"""
        self.click_element(self.__class__.__locators["发布新闻"])

    @TestLogger.log()
    def click_no_news(self):
        """点击未发新闻"""
        self.click_element(self.__class__.__locators["未发新闻"])

    @TestLogger.log()
    def click_link_publishing(self):
        """点击链接发布"""
        self.click_element(self.__class__.__locators["链接发布"])

    @TestLogger.log()
    def input_news_title(self, title):
        """输入新闻标题"""
        self.input_text(self.__class__.__locators["新闻标题"], title)

    @TestLogger.log()
    def input_link_news(self, url):
        """输入链接新闻"""
        self.input_text(self.__class__.__locators["链接新闻"], url)

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
    def is_exist_delete_successfully(self):
        """是否存在删除成功"""
        return self.is_toast_exist("删除成功")

    @TestLogger.log()
    def is_exist_no_news(self):
        """是否存在未发新闻"""
        els = self.get_elements(self.__class__.__locators["新闻标题选择框"])
        return len(els) > 0

    @TestLogger.log()
    def get_first_news_title(self):
        """获取第一条新闻的标题"""
        title = self.get_elements(self.__class__.__locators["新闻标题选择框"])[0].text
        return title

    @TestLogger.log()
    def click_first_news(self):
        """点击第一条新闻"""
        els = self.get_elements(self.__class__.__locators["新闻标题选择框"])
        if len(els) > 0:
            els[0].click()

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def is_exist_news_by_name(self, name):
        """是否存在指定新闻"""
        els = self.get_elements((MobileBy.XPATH, '//*[@resource-id="news_title" and @text="%s"]' % name))
        return len(els) > 0

