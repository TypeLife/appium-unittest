from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EmailListPage(BasePage):
    """邮件列表"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MailSummaryActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '列表标题': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
        '邮件列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '列表项': (MobileBy.XPATH, '//android.view.ViewGroup[.//*[@resource-id="com.chinasofti.rcs:id/mail_title"]]'),
        '查看全文': (MobileBy.ID, 'com.chinasofti.rcs:id/read_all'),
        '查看全文右箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/right_arrow_img'),
        '接收时间': (MobileBy.ID, 'com.chinasofti.rcs:id/send_time'),
        '信件主题': (MobileBy.ID, 'com.chinasofti.rcs:id/mail_title'),
        '信件内容简要': (MobileBy.ID, 'com.chinasofti.rcs:id/mail_summary'),
    }

    @TestLogger.log('点击返回上一页图标')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log("检查最新的一条邮件的主题")
    def assert_the_newest_email_is(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//android.view.ViewGroup[last()]//*[@resource-id="com.chinasofti.rcs:id/mail_title"]']
        # self.scroll_to_bottom()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(locator)[
                                    :len(title) if len(title) > 0 else None] in title,
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('{}秒内没有找到"{}"的最新消息'.format(max_wait_time, title))
