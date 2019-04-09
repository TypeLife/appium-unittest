from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeRecommentdClienPage(BasePage):
    """我-》推荐和飞信"""
    ACTIVITY = 'com.chinasofti.rcs/com.cmicc.module_aboutme.ui.activity.AboutActivity'

    __locators = {
        '推荐和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        # 推荐和飞信短信发送
        '发送': (MobileBy.ID, 'com.android.mms:id/send_button_sms'),
    }

    @TestLogger.log("等待推荐和飞信页面加载")
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["推荐和飞信"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log("检查该页面包含文本")
    def page_contain_text(self, menu):
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log('点击发送')
    def click_send(self):
        self.click_element(self.__locators["发送"])
